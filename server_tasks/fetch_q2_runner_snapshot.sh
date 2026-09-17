#!/usr/bin/env bash
# Mac-side transfer of one historical server script into a new private directory.
# Usage: bash server_tasks/fetch_q2_runner_snapshot.sh USER@HOST EXPECTED_SHA256
set -euo pipefail
umask 077
if [[ $# -ne 2 ]]; then
  echo "Usage: bash $0 USER@HOST EXPECTED_SHA256" >&2
  exit 2
fi
Q2_HOST=$1
Q2_EXPECTED=$2
[[ "$Q2_HOST" =~ ^[a-zA-Z0-9][a-zA-Z0-9._@-]*$ ]] || { echo 'Invalid host' >&2; exit 2; }
[[ "$Q2_EXPECTED" =~ ^[0-9a-f]{64}$ ]] || { echo 'Expected lowercase SHA256' >&2; exit 2; }
for tool in git scp shasum; do
  command -v "$tool" >/dev/null || { echo "Missing tool: $tool" >&2; exit 1; }
done
Q2_REPO=$(cd "$(dirname "$0")/.." && pwd)
git -C "$Q2_REPO" check-ignore -q data/processed/q2_server/provenance_probe/run_q2.sh || {
  echo 'Private destination is not gitignored; stopping.' >&2
  exit 1
}
mkdir -p "$Q2_REPO/data/processed/q2_server"
Q2_DEST=$(mktemp -d "$Q2_REPO/data/processed/q2_server/runner_snapshot_$(date -u +%Y%m%dT%H%M%SZ)_XXXXXX")
trap 'Q2_STATUS=$?; if [[ $Q2_STATUS -ne 0 ]]; then printf "Download/verification failed; unverified snapshot retained: %s\n" "$Q2_DEST" >&2; fi' EXIT
scp "${Q2_HOST}:/home/mva_q2/run_q2.sh" "$Q2_DEST/run_q2.sh"
Q2_ACTUAL=$(shasum -a 256 "$Q2_DEST/run_q2.sh")
Q2_ACTUAL=${Q2_ACTUAL%% *}
[[ "$Q2_ACTUAL" == "$Q2_EXPECTED" ]] || {
  echo 'FAIL: snapshot differs from the reported server hash; do not execute it.' >&2
  exit 1
}
printf 'PASS: downloaded script matches the reported SHA256; script was not executed.\n'
printf 'Local snapshot: %s/run_q2.sh\n' "$Q2_DEST"
printf 'Keep this source private; return only the local path, not the script contents.\n'
