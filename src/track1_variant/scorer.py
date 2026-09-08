#!/usr/bin/env python3
"""T1 本地评分 harness —— 官方 evaluation.py 内核 + 提交前校验与报告。

用法:
    python3 src/track1_variant/scorer.py <submission.csv> <truth.json>

truth.json 与官方 gold_standard_track1.json 同构（本地用合成数据，绝不含真实基因组）:
    {"PROBAND01": [["chr7", 7000001, "T", "G"], ["chrX", 8000002, "A", "C"]]}

分层设计:
  - 评分逻辑 100% 来自官方 references/official/evaluation.py（import，不转写，零抄写误差）
  - 本文件只加官方提交页 (tabs/submit_track1.py) 同款的前置校验 + 报告输出
  - 校验比官方更严: 强制完整 12 列表头（官方 DictReader 容忍缺列，模板即 12 列）

提交前必跑（G1/G2 门槛）。内核文件 SHA256 留档见 references/official/README.md。
"""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OFFICIAL_EVAL = REPO_ROOT / "references" / "official" / "evaluation.py"

# 官方模板 static/templates/track1_submission_template.csv 的 12 列（顺序固定）
EXPECTED_HEADER = [
    "proband_id", "chrom_1", "pos_1", "ref_1", "alt_1",
    "chrom_2", "pos_2", "ref_2", "alt_2",
    "epcr", "finding_type", "notes",
]
EXPECTED_PROBAND = "PROBAND01"  # 官方 submit_track1.py: "Only PROBAND01 is accepted"


def _load_official_kernel(path: Path = OFFICIAL_EVAL):
    """以模块方式加载官方 evaluation.py（评分逻辑的唯一权威来源）。"""
    spec = importlib.util.spec_from_file_location("official_evaluation", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["official_evaluation"] = module  # dataclasses 解析注解需要模块已注册
    spec.loader.exec_module(module)
    return module


ev = _load_official_kernel()


def preflight(csv_path: str | Path) -> list[str]:
    """官方提交页同款校验（返回错误列表；空列表 = 可安全消耗线上配额）。

    官方 _handle_submit / load_submission 的校验项:
      12 列表头齐全 · proband 仅 PROBAND01 · ≤10 行 · epcr ∈ (0,1]
      finding_type ∈ {primary, secondary}
    另加: epcr 未按降序排列时警告（官方仅排序不惩罚，但真实 CAGI 惯例预排序）。
    """
    errors: list[str] = []
    with open(csv_path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return ["CSV 为空文件"]
        if [h.strip() for h in header] != EXPECTED_HEADER:
            errors.append(f"表头不符: 应为 {EXPECTED_HEADER}，实为 {header}")

        rows = [r for r in reader if any(cell.strip() for cell in r)]

    if len(rows) > 10:
        errors.append(f"行数 {len(rows)} 超过上限 10")
    if not rows:
        errors.append("无数据行")

    epcrs: list[float] = []
    for i, row in enumerate(rows, start=2):  # 第 2 行起是数据
        if len(row) != len(EXPECTED_HEADER):
            errors.append(f"第 {i} 行列数 {len(row)} ≠ 12")
            continue
        pid = row[0].strip()
        if pid != EXPECTED_PROBAND:
            errors.append(f"第 {i} 行 proband_id='{pid}'，仅接受 {EXPECTED_PROBAND}")
        try:
            e = float(row[9])
            if not (0 < e <= 1):
                errors.append(f"第 {i} 行 epcr={e} 超出 (0,1]")
            epcrs.append(e)
        except ValueError:
            errors.append(f"第 {i} 行 epcr='{row[9]}' 不是数字")
        ft = (row[10] or "primary").strip().lower()
        if ft not in ("primary", "secondary"):
            errors.append(f"第 {i} 行 finding_type='{row[10]}' 应为 primary/secondary")
        if not row[1].strip() or not row[2].strip():
            errors.append(f"第 {i} 行缺少主变异 (chrom_1/pos_1)")

    if epcrs and epcrs != sorted(epcrs, reverse=True):
        print("⚠️  警告: epcr 未按降序排列（官方会代为排序，不扣分，但建议预排序）",
              file=sys.stderr)
    return errors


def load_truth(truth_path: str | Path) -> dict[str, frozenset]:
    """加载本地合成 truth JSON（结构同官方 groundtruth.load_groundtruth 的产物）。"""
    raw = json.loads(Path(truth_path).read_text())
    return {
        pid: frozenset((str(c), int(p), str(r).upper(), str(a).upper()) for c, p, r, a in variants)
        for pid, variants in raw.items()
    }


def run(csv_path: str | Path, truth_path: str | Path) -> tuple[object, int]:
    """校验 + 评分。返回 (exit_code, ScoreResult)；校验失败 exit_code=1。"""
    errors = preflight(csv_path)
    if errors:
        print("❌ 提交前校验未通过（不要消耗线上配额）:")
        for e in errors:
            print(f"   - {e}")
        return None, 1

    truth = load_truth(truth_path)
    submissions = ev.load_submission(str(csv_path))
    pid = next(iter(submissions))
    if pid not in truth:
        print(f"❌ truth 中无 {pid}")
        return None, 1
    result = ev.score_proband(pid, submissions[pid], truth[pid])

    match_desc = (
        f"✅ Full match at rank {result.full_match_rank}"
        if result.full_match_rank is not None
        else (
            f"⚠️ Partial match (one of two comp-het variants) at rank {result.partial_match_rank}"
            if result.partial_match_rank is not None
            else "❌ No match"
        )
    )
    print(f"proband: {result.proband_id}")
    print(f"rank_points : {result.rank_points:.1f} / 100")
    print(f"F-max       : {result.f_max:.3f}  (threshold={result.f_max_threshold}, "
          f"n_rows={result.n_predictions_at_f_max})")
    print(match_desc)
    return result, 0


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    _, code = run(argv[1], argv[2])
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
