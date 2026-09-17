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
  R6 granularity 只能是 public | report；两者均不授权公开位点级内容
  R7 fact 节点不得引用 claim_type=hypothesis 的 EV（禁止静默升格）
  R8 扫描 reports/*.md 的 [EV-xxxx]：须在公开台账或私有附录白名单；括号内不得夹裸数字（缺 EV- 前缀）
  R9 claim 清单不得为空；每条 claim 必须有合法、非空 EV 引用和对应报告文本。

这些是结构与引用检查，不验证文献是否支持句意，也不证明 claim 清单覆盖所有断言。

这是 M5 对抗审查门的第二道自动化关卡（第一道是 ledger.py lint）。
"""

from __future__ import annotations

import json
import csv
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHAIN = REPO_ROOT / "research" / "mechanism_chain.json"
LEDGER = REPO_ROOT / "research" / "evidence.jsonl"
REPORTS = REPO_ROOT / "reports"
CLAIMS = REPO_ROOT / "research" / "report_claims.tsv"
PRIVATE_LEDGER = REPO_ROOT / "data" / "processed" / "evidence_private.jsonl"
# 位点/核型级条目只存在于 gitignored 私有附录；公开报告可引用 ID，数值不进公开仓。
PRIVATE_APPENDIX = frozenset({"EV-0039", "EV-0040", "EV-0077", "EV-0086"})
EV_ID_RE = re.compile(r"EV-\d{4}")
BRACKET_RE = re.compile(r"\[([^\]]+)\]")
# 只抓 EV 风格的裸编号（0051），避免把 2017 等年份当缺前缀。
BARE_EV_NUM_RE = re.compile(r"(?<!EV-)\b0\d{3}\b")


def main() -> None:
    dot = "--dot" in sys.argv
    with CHAIN.open(encoding="utf-8") as handle:
        chain = json.load(handle)
    evs = {}
    with open(LEDGER) as f:
        for line in f:
            if line.strip():
                e = json.loads(line)
                evs[e["id"]] = e
    private_evs = {}
    if PRIVATE_LEDGER.exists():
        with open(PRIVATE_LEDGER) as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    private_evs[entry["id"]] = entry
    errors = []

    nodes = {n["id"]: n for n in chain["nodes"]}
    warns = []

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
        if n.get("claim_type") == "fact":
            for r in refs:
                ev = evs.get(r)
                if ev and ev.get("verification_status") == "unverified":
                    errors.append(f"{nid}: R2 fact 引用了非 verified 条目 {r}")
                if ev and ev.get("verification_status") == "conflict" and not n.get("conflict_note"):
                    errors.append(f"{nid}: R2 fact 引用 conflict 条目但未披露 {r}")
        if n.get("claim_type") == "hypothesis" and not (n.get("counter_note") or n.get("conflict_note")):
            errors.append(f"{nid}: R4 hypothesis 缺 counter_note/conflict_note")
        if n.get("claim_type") == "fact":
            for r in refs:
                ev = evs.get(r)
                if ev and ev.get("claim_type") == "hypothesis":
                    errors.append(f"{nid}: R7 fact 节点引用了 hypothesis 条目 {r}（禁止升格）")

    if not dot:
        for path in sorted(REPORTS.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(REPO_ROOT)
            for m in BRACKET_RE.finditer(text):
                inner = m.group(1)
                if "EV-" not in inner and not re.search(r"\b0\d{3}\b", inner):
                    continue
                if BARE_EV_NUM_RE.search(inner):
                    errors.append(f"R8 {rel}: 引用缺 EV- 前缀: [{inner}]")
                for eid in EV_ID_RE.findall(inner):
                    if eid not in evs and eid not in PRIVATE_APPENDIX:
                        errors.append(f"R8 {rel}: 引用不在公开台账或私有附录白名单: {eid}")
                    elif eid in PRIVATE_APPENDIX and eid not in private_evs:
                        errors.append(f"R8 {rel}: 白名单私有条目实际缺失: {eid}")
            for eid in EV_ID_RE.findall(text):
                if eid not in evs and eid not in PRIVATE_APPENDIX:
                    errors.append(f"R8 {rel}: 正文 {eid} 不在公开台账或私有附录白名单")
                elif eid in PRIVATE_APPENDIX and eid not in private_evs:
                    errors.append(f"R8 {rel}: 正文引用的私有条目实际缺失: {eid}")

        if not CLAIMS.exists():
            errors.append("R9: 缺少 research/report_claims.tsv")
        else:
            with open(CLAIMS, encoding="utf-8") as handle:
                claims = list(csv.DictReader(handle, delimiter="\t"))
            if not claims:
                errors.append("R9: claim 清单为空")
            seen_claims = set()
            allowed_types = {"fact", "inference", "research_hypothesis"}
            for claim in claims:
                cid = (claim.get("claim_id") or "").strip()
                if not cid:
                    errors.append("R9: claim_id 为空")
                if len(claim.get("claim_text", "").strip()) < 12:
                    errors.append(f"R9 {cid}: claim_text 过短或为空")
                if cid in seen_claims:
                    errors.append(f"R9: claim id 重复 {cid}")
                seen_claims.add(cid)
                if claim.get("claim_type") not in allowed_types:
                    errors.append(f"R9 {cid}: 非法 claim_type")
                report = REPO_ROOT / claim.get("report_file", "")
                if not report.exists() or claim.get("claim_text", "") not in report.read_text(encoding="utf-8"):
                    errors.append(f"R9 {cid}: claim_text 未在指定报告找到")
                refs = [x.strip() for x in (claim.get("ev_refs") or "").split(";") if x.strip()]
                if not refs:
                    errors.append(f"R9 {cid}: 无 ev_refs")
                for ref in refs:
                    if not EV_ID_RE.fullmatch(ref):
                        errors.append(f"R9 {cid}: 非法 EV 引用 {ref!r}")
                        continue
                    entry = evs.get(ref) or (private_evs.get(ref) if ref in PRIVATE_APPENDIX else None)
                    if not entry:
                        errors.append(f"R9 {cid}: 缺失 {ref}")
                    elif claim.get("claim_type") == "fact" and entry.get("verification_status") != "verified":
                        errors.append(f"R9 {cid}: fact 引用了非 verified 的 {ref}")
                if claim.get("claim_type") in {"inference", "research_hypothesis"} and not claim.get("translation_note"):
                    errors.append(f"R9 {cid}: 推断/假设缺 translation_note")
                if claim.get("quantitative") == "yes" and claim.get("power_basis") in {"", "NA"}:
                    errors.append(f"R9 {cid}: 定量 claim 缺 power_basis")
                if claim.get("review_status") != "independent_reviewed":
                    warns.append(f"R9 {cid}: 尚未独立审核（{claim.get('review_status')}）")

    if dot:
        print("digraph mechanism { rankdir=LR;")
        for n in chain["nodes"]:
            shape = "box" if n.get("granularity") == "report" else "ellipse"
            print(f'  {n["id"]} [label="{n["id"]}: {n["stage"]}", shape={shape}];')
        for a, b in chain["edges"]:
            print(f"  {a} -> {b};")
        print("}")
        return

    errors = list(dict.fromkeys(errors))
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
