#!/usr/bin/env python3
"""M2 候选药物评分 —— drug_pool.tsv × docs/09 档案 → 排序候选表（可复现）。

用法:
    python3 src/track2_repurposing/score_candidates.py

输入:  data/processed/track2/drug_pool.tsv   （build_drug_pool.py 产出，gitignored）
       docs/09-M2候选档案.md                 （人工策展的评分依据，见下方 CANDIDATES 溯源）
输出:  data/processed/track2/candidates_ranked.tsv（gitignored）+ stdout 摘要

评分维度（0–3 整数，依据与 EV 溯源内嵌；总分 = 加权和）:
  mechanism_match  0-3   与机制链 node 的连线强度（3=直打核心节点且有人体/模型直接证据）
  testable_pred    0-3   可检验预测的可落地性（3=有现成模型平台 + 可测读出）
  evidence_human   0-3   已上市端人体证据强度（3=RCT 级）
  safety_margin    0-3   儿科慢程使用的安全性余地（3=广泛儿科经验；反向计分负担）
  counter_weight   0-3   反面证据的可反驳性（3=主要反面可在设计层面规避）

权重: mechanism_match ×2, 其余 ×1 —— 机制匹配是 T2 评审的根基（Rigor 35%）。
精选规则: top-N（N≤5）且每候选独立机制轴；同轴次名降为 alternate。
"""

from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POOL = REPO / "data" / "processed" / "track2" / "drug_pool.tsv"
OUT = REPO / "data" / "processed" / "track2" / "candidates_ranked.tsv"

# 人工策展评分（依据 docs/09-M2候选档案.md §2/§3；每字段带一句话理由 + EV）
CANDIDATES = {
    "niacinamide (nicotinamide)": dict(
        axis="L1_protein_stability",
        mechanism_match=3,  # 唯一直打 N5（BUBR1 蛋白不足）[EV-0066,0067]
        testable_pred=3,    # 蛋白丰度读出直接可测 + 线虫平台 [EV-0023,0080]
        evidence_human=3,   # ONTRAC III 期 RCT [EV-0070]
        safety_margin=3,    # OTC/注射复合维生素儿科剂型 [EV-0069]
        counter_weight=2,   # NMN→niacinamide 平移距离须明示 [EV-0066 counter]
        rationale="SIRT2–NAD+ axis raises BubR1 abundance in vivo; approved precursor with RCT precedent",
    ),
    "everolimus": dict(
        axis="L2_mtorc1_sarcopenia",
        mechanism_match=2,  # N11 轴小鼠级 [EV-0057]
        testable_pred=2,    # daf-15/Raptor 可操作 [EV-0074,0081]
        evidence_human=3,   # 儿科起病 15.5 年队列 + 标签≥1 岁 [EV-0079,0078]
        safety_margin=1,    # 代谢 ADR 谱 + 免疫抑制 [EV-0079 counter]
        counter_weight=2,   # 生长终点空白=诚实开放问题 [EV-0059,0079]
        rationale="mTORC1 hyperactivity-sarcopenia axis; deepest pediatric mTORi experience",
    ),
    "metformin": dict(
        axis="L4_metabolic_systemic_stress",
        mechanism_match=2,  # N13 + 非整倍体代谢脆弱 [EV-0061,0072]
        testable_pred=3,    # 线虫跨物种先例 + 生物标志物 [EV-0073,0080]
        evidence_human=2,   # 儿科广泛使用（PCOS 等），非 RCT 于本轴
        safety_margin=3,    # 儿科长期安全性轮廓成熟
        counter_weight=2,   # 与 L3 清除方向张力按场景拆分 [EV-0063 vs 0072/0073]
        rationale="Approved AMPK/energy-state modulator; cross-species aneuploidy-model protection",
    ),
    "chloroquine": dict(
        axis="L3_aneuploidy_clearance",
        mechanism_match=3,  # 唯一 MVA 模型直接证据 [EV-0063]
        testable_pred=2,    # 患者细胞可测；体内肿瘤终点难 [EV-0063 counter]
        evidence_human=1,   # 老药但本轴无人体试验
        safety_margin=1,    # 视网膜毒性/儿科长期负担
        counter_weight=2,   # 细胞级证据局限明确可述
        rationale="Selective anti-aneuploid proliferation, validated on BubR1H/H MVA-model MEFs",
    ),
    "sirolimus": dict(
        axis="L2_mtorc1_sarcopenia",
        mechanism_match=2,  # 同 everolimus 轴 [EV-0057]
        testable_pred=2,    # 同轴 [EV-0074]
        evidence_human=2,   # Becker 队列含 sirolimus 4 例 [EV-0079]
        safety_margin=1,    # 同轴免疫抑制负担
        counter_weight=1,   # 同轴且儿科经验弱于 everolimus
        rationale="Same-axis alternate to everolimus (pediatric experience shallower)",
    ),
    "hydroxychloroquine": dict(
        axis="L3_aneuploidy_clearance",
        mechanism_match=2,  # 同轴衍生物，零 MVA 模型数据 [EV-0063]
        testable_pred=2,    # 同轴
        evidence_human=1,   # 本轴无人体试验
        safety_margin=2,    # 视网膜毒性低于 CQ
        counter_weight=2,   # 轴内首选保留有直接证据的 CQ
        rationale="Tolerability-optimized alternate (no MVA-model data)",
    ),
}

WEIGHTS = {"mechanism_match": 2, "testable_pred": 1,
           "evidence_human": 1, "safety_margin": 1, "counter_weight": 1}


def main() -> None:
    pool = {}
    with open(POOL) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            pool[row["drug_name"]] = row

    scored = []
    for name, c in CANDIDATES.items():
        approved = pool.get(name, {}).get("us_status", "missing")
        if approved != "us_approved":
            print(f"!! {name}: 上市核验状态 {approved} —— 红线候选不应出现于此", file=__import__("sys").stderr)
        total = sum(c[k] * WEIGHTS[k] for k in WEIGHTS)
        scored.append((total, name, approved, c))

    scored.sort(key=lambda t: (-t[0], t[1]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w") as f:
        f.write("drug\taxis\ttotal\tmechanism_match(x2)\ttestable_pred\tevidence_human\t"
                "safety_margin\tcounter_weight\tus_status\trationale\n")
        for total, name, approved, c in scored:
            f.write("\t".join(map(str, [name, c["axis"], total, c["mechanism_match"] * 2,
                                        c["testable_pred"], c["evidence_human"],
                                        c["safety_margin"], c["counter_weight"],
                                        approved, c["rationale"]])) + "\n")

    print(f"{'drug':32s} {'axis':28s} {'score':>5s}  status")
    for total, name, approved, c in scored:
        print(f"{name:32s} {c['axis']:28s} {total:5d}  {approved}")
    print(f"\n→ {OUT}")
    print("精选 = 前 4（独立轴）；sirolimus/HCQ 为同轴 alternate（见 docs/09 §4）")


if __name__ == "__main__":
    main()
