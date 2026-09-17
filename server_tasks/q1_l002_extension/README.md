# L002 Q1 follow-up: standalone analysis

Run on the existing controlled Linux server with minimap2 2.31-r1302,
samtools 1.9 and Python 3.9+. This is a follow-up design specified before
examining L002 candidate results. It is not the original preregistration.

`bash run.sh /home/mva_q2` creates a unique private run directory, acquires
a nonblocking lock, verifies the previously recorded reference/target/L002
and validator hashes, and requires 20 GiB available RAM and 180 GiB free disk.
The existing L001 BAMs are read only. No download or automatic deletion occurs.

Alignment uses the same minimap2 parameters and mapped-read policy as Q2.
L002 gets its own RG/PU and the known sample ID, but no invented library ID.
Name sort -> fixmate -> coordinate sort -> markdup (retain flags) -> duplicate
filtering produces L002 before/after results. Sort uses two extra threads and
1 GiB per thread; alignment uses twelve threads. Native minimap2 index/mapping
memory is additional and is not a hard memory cap.

The frozen prior Q1 validator is hash checked and reused for both lanes.
Original support thresholds (ALT >=5, ALT/(REF+ALT) in [0.30,0.70]) and the
later-added zero-mate-conflict criterion are reported separately. Read-name
deduplication and alignment-duplicate filtering are distinct operations.
This package does NOT merge lanes or assume verified common library origin.
No shared qualified query name means direct phase was not established, not
proof that all possible chained short-read phasing methods are impossible.

Keep details, BAMs and logs in the controlled server environment. Return only
the explicitly allowlisted `q1_l002_return_bundle.tar.gz` from the unique run.
Completion denotes an executed analysis, not that both candidates passed.

Tests use synthetic alleles/reads and do not inspect controlled data.
