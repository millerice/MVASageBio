#!/usr/bin/env bash
# Run on the Mac: bash server_tasks/fetch_q1_diagnostics.sh USER@HOST /absolute/path/diagnostic_return.tar.gz
# Download only the named archive; keep every transfer in a new gitignored directory.
set -euo pipefail
umask 077

if [[ $# -ne 2 ]]; then
  echo "Usage: bash $0 USER@HOST /absolute/path/diagnostic_return.tar.gz" >&2
  exit 2
fi
Q1_REMOTE=$1
Q1_REMOTE_FILE=$2
[[ "$Q1_REMOTE" =~ ^[a-zA-Z0-9][a-zA-Z0-9._@-]*$ ]] || { echo 'Invalid host' >&2; exit 2; }
[[ "$Q1_REMOTE_FILE" =~ ^/[a-zA-Z0-9_./-]+/diagnostic_return\.tar\.gz$ ]] || { echo 'Expected an absolute diagnostic_return.tar.gz path' >&2; exit 2; }
for tool in scp python3 git; do
  command -v "$tool" >/dev/null || { echo "Missing tool: $tool" >&2; exit 1; }
done
Q1_REPO=$(cd "$(dirname "$0")/.." && pwd)
git -C "$Q1_REPO" check-ignore -q data/processed/q2_server/diagnostic_archive_probe/file.json || {
  echo 'Private destination is not gitignored; stopping.' >&2
  exit 1
}
Q1_BASE=$Q1_REPO/data/processed/q2_server
mkdir -p "$Q1_BASE"
Q1_LOCAL=$(mktemp -d "$Q1_BASE/diagnostic_archive_$(date -u +%Y%m%dT%H%M%SZ)_XXXXXX")
trap 'Q1_STATUS=$?; if [[ $Q1_STATUS -ne 0 ]]; then printf "Transfer/validation failed; unverified files retained in: %s\n" "$Q1_LOCAL" >&2; fi' EXIT
printf 'Downloading into: %s\n' "$Q1_LOCAL"
scp "${Q1_REMOTE}:${Q1_REMOTE_FILE}" "$Q1_LOCAL/diagnostic_return.tar.gz"

python3 -B - "$Q1_LOCAL" <<'PY'
import hashlib
import json
import re
import sys
import tarfile
from pathlib import Path

destination = Path(sys.argv[1])
names = {
    "q1_local_diagnostic_safe.json",
    "q1_balance_safe.json",
    "q1_strand_safe.json",
}
allowed = names | {"RETURN_CHECKSUMS.sha256"}
contents = {}
with tarfile.open(destination / "diagnostic_return.tar.gz", "r:gz") as archive:
    for member in archive:
        # Do not extract links, directories, extra files or paths outside this directory.
        if member.name not in allowed or member.name in contents or not member.isfile():
            raise SystemExit("FAIL: archive contains an unexpected member/type")
        if not 0 < member.size <= 10 * 1024 * 1024:
            raise SystemExit("FAIL: unexpected member size")
        contents[member.name] = archive.extractfile(member).read()
if set(contents) != allowed:
    raise SystemExit("FAIL: archive is missing required files")

checksums = {}
for line in contents["RETURN_CHECKSUMS.sha256"].decode("ascii").splitlines():
    match = re.fullmatch(r"([0-9a-fA-F]{64}) [ *](\S+)", line)
    if not match or match[2] not in names or match[2] in checksums:
        raise SystemExit("FAIL: invalid checksum manifest")
    checksums[match[2]] = match[1].lower()
if set(checksums) != names:
    raise SystemExit("FAIL: incomplete checksum manifest")
for name in sorted(names):
    if hashlib.sha256(contents[name]).hexdigest() != checksums[name]:
        raise SystemExit("FAIL: checksum mismatch for " + name)
    if not isinstance(json.loads(contents[name]), dict):
        raise SystemExit("FAIL: expected a JSON object in " + name)

# Write only after every member has passed validation; never overwrite a file.
for name in sorted(allowed):
    with (destination / name).open("xb") as handle:
        handle.write(contents[name])
print("PASS: expected files, all three SHA256 checksums, and JSON syntax")
print("Local directory: " + str(destination))
print("Archive validation does not establish scientific validity or complete de-identification.")
PY
