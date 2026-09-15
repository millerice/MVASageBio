#!/usr/bin/env python3
"""M2 药池构建 + 上市状态自动核验（openFDA drugsfda，Tier 0）。

用法:
    python3 src/track2_repurposing/build_drug_pool.py            # 核验种子表 → drug_pool.tsv
    python3 src/track2_repurposing/build_drug_pool.py --dry-run  # 只列种子与数据源计划

输入:  research/drug_candidates_seed.tsv   （人工策展，repo 安全：药名/杠杆/EV 依据）
输出:  data/processed/track2/drug_pool.tsv（gitignored；核验结果含 US 辖区判定）

核验逻辑（CLAUDE.md 红线 #5「只提名已上市药物」的自动化）:
  - openFDA drugsfda（官方 API，无需 key）按 generic name / active ingredient 检索
  - 存在 ≥1 个产品 marketing_status ∈ {Prescription, Over-the-counter}（即非全部 Discontinued）
    → US-approved；全 Discontinued → discontinued_only；零命中 → not_found
  - 附条件批准/辖区差异无法从该 API 完整判定 → 输出 needs_manual_check 列，
    M3 报告期人工补 EMA/附条件状态（口径：FDA + EMA 双源）

排除行不删——留在池中标记 excluded_*，作为报告「为什么不是它」的叙事素材。
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SEED = REPO_ROOT / "research" / "drug_candidates_seed.tsv"
OUT = REPO_ROOT / "data" / "processed" / "track2" / "drug_pool.tsv"
API = "https://api.fda.gov/drug/drugsfda.json"
MARKETED = {"Prescription", "Over-the-counter"}


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "MVASageBio-T2/0.1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def safe_query(url: str) -> dict:
    """openFDA 对零命中返回 HTTP 404（带 JSON 错误体）——按『无结果』处理，非网络错误。"""
    try:
        return fetch_json(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"results": []}
        raise


def verify(name: str) -> dict:
    """drugsfda 按 generic name / 活性成分检索并判定上市状态。"""
    q = urllib.parse.quote(f'"{name.split(" (")[0]}"')
    hits, marketed = 0, 0
    for field in ("openfda.generic_name", "products.active_ingredients.name"):
        url = f"{API}?search={field}:{q}&limit=20"
        try:
            data = safe_query(url)
        except Exception as e:  # noqa: BLE001 —— 单源失败不终止整池
            return {"status": "api_error", "apps": 0, "marketed_products": 0,
                    "needs_manual_check": f"openFDA {field} 查询失败: {e}"}
        for app in data.get("results", []):
            hits += 1
            for prod in app.get("products", []):
                if prod.get("marketing_status") in MARKETED:
                    marketed += 1
        if hits:
            break  # generic_name 命中即不再查活性成分
    if not hits:
        verdict = "not_found"
    elif marketed:
        verdict = "us_approved"
    else:
        verdict = "discontinued_only"
    return {"status": verdict, "apps": hits, "marketed_products": marketed,
            "needs_manual_check": "" if verdict == "us_approved" else "EMA/辖区状态人工补查"}


def main() -> None:
    if "--dry-run" in sys.argv:
        print("种子表（research/drug_candidates_seed.tsv）:")
        for line in SEED.read_text().splitlines():
            print("  " + line.split("\t")[0] + "\t" + line.split("\t")[1])
        print("\n核验源: openFDA drugsfda (https://api.fda.gov)，判定口径见文件头注释")
        return

    rows = [l.split("\t") for l in SEED.read_text().splitlines() if l.strip()]
    header, data = rows[0], rows[1:]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out = ["\t".join(header + ["us_status", "us_apps", "us_marketed_products",
                               "needs_manual_check", "retrieved_at"])]
    from datetime import date
    today = date.today().isoformat()
    for r in data:
        name = r[0]
        res = verify(name)
        print(f"  {name:42s} → {res['status']:18s} (apps={res['apps']}, "
              f"marketed={res['marketed_products']})")
        out.append("\t".join(r + [res["status"], str(res["apps"]),
                                  str(res["marketed_products"]),
                                  res["needs_manual_check"], today]))
    OUT.write_text("\n".join(out) + "\n")
    print(f"\n→ {OUT}（{len(data)} 行核验完成）")


if __name__ == "__main__":
    main()
