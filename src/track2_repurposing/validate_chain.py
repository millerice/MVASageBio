#!/usr/bin/env python3
"""机制链校验器 —— research/mechanism_chain.json × research/evidence.jsonl 交叉审计。

用法:
    python3 src/track2_repurposing/validate_chain.py          # 校验（错误退出码非 0）
    python3 src/track2_repurposing/validate_chain.py --dot    # 输出 graphviz DOT（画机制图用）

校验规则（把 CLAUDE.md 证据规则变成可执行门槛）:
  R1 每条 node 的每个 ev_refs 必须存在于台账
  R2 fact 类 node 至少引用 1 条 tier ≤ 1 的 EV（权威级支撑）
  R3 引用 verification_status=conflict 的 EV 时，node 必须带 conflict_note
  R4 hypothesis 类 node 不得只靠 fact 级表述混过——必须有 counter_note 或 counter 类 EV
  R5 node id 唯一、edges 两端都是存在的 node、无孤立 node
  R6 granularity 只能是 public | report；report 级内容提示「只进提交报告，不进公开 repo」

这是 M5 对抗审查门的第二道自动化关卡（第一道是 ledger.py lint）。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHAIN = REPO_ROOT / "research" / "mechanism_chain.json"
LEDGER = REPO_ROOT / "research" / "evidence.jsonl"


def main() -> None:
    dot = "--dot" in sys.argv
    chain = json.load(open(CHAIN))
    evs = {}
    with open(LEDGER) as f:
        for line in f:
            if line.strip():
                e = json.loads(line)
                evs[e["id"]] = e

    nodes = {n["id"]: n for n in chain["nodes"]}
    errors, warns = [], []

    ids = [n["id"] for n in chain["nodes"]]
    if len(ids) != len(set(ids)):
        errors.append("R5: node id 重复")

    referenced = set()
    for a, b in chain["edges"]:
        if a not in nodes or b not in nodes:
            errors.append(f"R5: edge {a}->{b} 指向不存在的 node")
        referenced.update((a, b))
    for nid in nodes:
        if nid not in referenced:
            warns.append(f"R5: 孤立 node {nid}（无边连接）")

    for n in chain["nodes"]:
        nid = n["id"]
        if n.get("granularity") not in {"public", "report"}:
            errors.append(f"{nid}: granularity 非法 {n.get('granularity')!r}")
        refs = n.get("ev_refs", [])
        if not refs:
            errors.append(f"{nid}: R1 无 ev_refs")
        has_tier1 = False
        for r in refs:
            ev = evs.get(r)
            if ev is None:
                errors.append(f"{nid}: R1 ev_refs 引用不存在的 {r}")
                continue
            if ev.get("tier", 9) <= 1:
                has_tier1 = True
            if ev.get("verification_status") == "conflict" and not n.get("conflict_note"):
                errors.append(f"{nid}: R3 引用 conflict 条目 {r} 但缺 conflict_note")
        if n.get("claim_type") == "fact" and refs and not has_tier1:
            errors.append(f"{nid}: R2 fact 断言缺少 tier≤1 的权威支撑")
        if n.get("claim_type") == "hypothesis" and not (n.get("counter_note") or n.get("conflict_note")):
            errors.append(f"{nid}: R4 hypothesis 缺 counter_note/conflict_note")

    if dot:
        print("digraph mechanism { rankdir=LR;")
        for n in chain["nodes"]:
            shape = "box" if n.get("granularity") == "report" else "ellipse"
            print(f'  {n["id"]} [label="{n["id"]}: {n["stage"]}", shape={shape}];')
        for a, b in chain["edges"]:
            print(f"  {a} -> {b};")
        print("}")
        return

    for w in warns:
        print(f"⚠ {w}")
    if errors:
        print(f"✗ 机制链校验失败 {len(errors)} 处:")
        for x in errors:
            print(f"  - {x}")
        sys.exit(1)
    n_pub = sum(1 for n in chain["nodes"] if n.get("granularity") == "public")
    print(f"✓ 机制链校验通过：{len(nodes)} nodes（public {n_pub} / report {len(nodes)-n_pub}），"
          f"{len(chain['edges'])} edges，ev_refs 全部溯源成功")


if __name__ == "__main__":
    main()
