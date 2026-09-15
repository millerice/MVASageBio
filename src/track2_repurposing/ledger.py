#!/usr/bin/env python3
"""证据台账 CLI —— research/evidence.jsonl 的 lint / stats / show / grep。

用法:
    python3 src/track2_repurposing/ledger.py lint      # schema 校验全部条目（提交前必跑）
    python3 src/track2_repurposing/ledger.py stats     # 各维度统计（含 conflict/unverified 计数）
    python3 src/track2_repurposing/ledger.py show EV-0045   # 单条 pretty print
    python3 src/track2_repurposing/ledger.py grep mTORC1    # claim/evidence 检索

设计约束（CLAUDE.md 证据规则）:
  - 只读公开台账 research/evidence.jsonl；私有台账（变异级）在 data/processed/，永不入 git，本工具不触碰
  - lint 是 M5 对抗审查门的第一道自动化关卡：schema 错误退出码非 0
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LEDGER = REPO_ROOT / "research" / "evidence.jsonl"

DOMAINS = {"competition", "battlefield", "disease", "therapy", "strategy"}
CLAIM_TYPES = {"fact", "inference", "hypothesis", "strategic_opinion"}
STATUSES = {"verified", "unverified", "conflict"}
REQUIRED = ["id", "domain", "claim", "claim_type", "tier", "source", "evidence",
            "confidence", "verification_status"]
ID_RE = re.compile(r"^EV-\d{4}$")


def load() -> list[dict]:
    entries = []
    with open(LEDGER) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                sys.exit(f"FATAL 第 {i} 行 JSON 解析失败: {e}")
    return entries


def lint(entries: list[dict]) -> int:
    errors, seen = [], set()
    for e in entries:
        eid = e.get("id", "??")
        for k in REQUIRED:
            if k not in e or e[k] in (None, ""):
                errors.append(f"{eid}: 缺必填字段 {k}")
        if not ID_RE.match(str(eid)):
            errors.append(f"{eid}: id 格式应为 EV-XXXX")
        if eid in seen:
            errors.append(f"{eid}: id 重复")
        seen.add(eid)
        if e.get("domain") not in DOMAINS:
            errors.append(f"{eid}: domain 非法 {e.get('domain')!r}")
        if e.get("claim_type") not in CLAIM_TYPES:
            errors.append(f"{eid}: claim_type 非法 {e.get('claim_type')!r}")
        if e.get("verification_status") not in STATUSES:
            errors.append(f"{eid}: verification_status 非法 {e.get('verification_status')!r}")
        t = e.get("tier")
        if not isinstance(t, int) or not 0 <= t <= 4:
            errors.append(f"{eid}: tier 应为 0-4 整数， got {t!r}")
        c = e.get("confidence")
        if not isinstance(c, (int, float)) or not 0 <= c <= 1:
            errors.append(f"{eid}: confidence 应为 0-1， got {c!r}")
        for k in ("title", "url"):
            if not isinstance(e.get("source"), dict) or not e["source"].get(k):
                errors.append(f"{eid}: source.{k} 缺失")
    ids = [e["id"] for e in entries if ID_RE.match(str(e.get("id", "")))]
    nums = [int(x[-4:]) for x in ids]
    if nums != sorted(nums):
        errors.append(f"id 序列非递增（不强制连号，强制有序）")
    if errors:
        print(f"✗ lint 失败 {len(errors)} 处:")
        for x in errors:
            print(f"  - {x}")
        return 1
    print(f"✓ lint 通过：{len(entries)} 条，id {ids[0]} ~ {ids[-1]}")
    return 0


def stats(entries: list[dict]) -> None:
    def count(key):
        out = {}
        for e in entries:
            out[e.get(key)] = out.get(e.get(key), 0) + 1
        return dict(sorted(out.items(), key=lambda kv: str(kv[0])))

    print(f"总条目: {len(entries)}")
    for key, label in [("domain", "域"), ("claim_type", "类型"), ("tier", "层级"),
                       ("verification_status", "状态")]:
        print(f"{label}: {count(key)}")
    flagged = [e["id"] for e in entries if e.get("verification_status") != "verified"]
    print(f"非 verified（报告引用需注意）: {flagged or '无'}")


def show(entries: list[dict], eid: str) -> None:
    for e in entries:
        if e.get("id") == eid:
            print(json.dumps(e, ensure_ascii=False, indent=2))
            return
    sys.exit(f"未找到 {eid}")


def grep(entries: list[dict], term: str) -> None:
    hits = [e for e in entries
            if term.lower() in json.dumps(e, ensure_ascii=False).lower()]
    for e in hits:
        print(f"{e['id']} [{e.get('verification_status')}] {e['claim'][:100]}")
    print(f"— {len(hits)} 命中")


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in {"lint", "stats", "show", "grep"}:
        sys.exit(__doc__)
    entries = load()
    cmd = sys.argv[1]
    if cmd == "lint":
        sys.exit(lint(entries))
    if cmd == "stats":
        stats(entries)
    elif cmd == "show":
        show(entries, sys.argv[2])
    elif cmd == "grep":
        grep(entries, sys.argv[2])


if __name__ == "__main__":
    main()
