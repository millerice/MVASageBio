#!/usr/bin/env python3
"""scorer.py 测试套件 —— G1 门槛"本地评分器全绿"的验收测试。

全部使用合成数据（染色体/坐标为编造，与真实患儿数据无关；基因组数据绝不入 git）。
覆盖: 格式校验 / 档位计分 / comp-het 半分 / F-max 扫描 / 排序规则 / 规范化陷阱。

运行: python3 src/track1_variant/test_scorer.py
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scorer  # noqa: E402

HEADER = scorer.EXPECTED_HEADER
# 合成 comp-het 答案（与真实答案无关）
V1 = ("chr7", 7000001, "T", "G")
V2 = ("chrX", 8000002, "A", "C")
WRONG = ("chr1", 111111, "C", "T")
TRUTH = {"PROBAND01": frozenset([V1, V2])}


def write_csv(rows, path, header=HEADER):
    import csv
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    return str(path)


def comp_het_row(v1, v2, epcr, finding="primary", note=""):
    return ["PROBAND01", v1[0], v1[1], v1[2], v1[3],
            v2[0], v2[1], v2[2], v2[3], epcr, finding, note]


def single_row(v, epcr, finding="primary", note=""):
    return ["PROBAND01", v[0], v[1], v[2], v[3], "", "", "", "", epcr, finding, note]


def row_with_chrom(chrom, v, epcr):
    """替换 comp-het 行第一变异的染色体表示（其余不变）。"""
    r = comp_het_row(v, V2, epcr)
    r[1] = chrom
    return r


class HarnessTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.truth_path = Path(self.tmp) / "truth.json"
        self.truth_path.write_text(json.dumps(
            {"PROBAND01": [list(V1), list(V2)]}))

    def score(self, rows, header=HEADER):
        """官方内核评分（跳过 preflight，用于隔离测试评分逻辑本身）。"""
        csv_path = write_csv(rows, Path(self.tmp) / "sub.csv", header)
        subs = scorer.ev.load_submission(csv_path)
        return scorer.ev.score_proband("PROBAND01", subs["PROBAND01"], TRUTH["PROBAND01"])

    def run_harness(self, rows, header=HEADER):
        """完整流程: preflight + 评分，返回 (result, exit_code, stdout)。"""
        csv_path = write_csv(rows, Path(self.tmp) / "sub.csv", header)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result, code = scorer.run(csv_path, self.truth_path)
        return result, code, buf.getvalue()


# ---------- 档位计分 ----------

class TestRankTiers(HarnessTestCase):
    def test_full_match_rank1_100(self):
        r = self.score([comp_het_row(V1, V2, 0.9)])
        self.assertEqual(r.rank_points, 100.0)
        self.assertEqual(r.full_match_rank, 1)
        self.assertIsNone(r.partial_match_rank)

    def test_full_match_rank2_50(self):
        r = self.score([single_row(WRONG, 0.95), comp_het_row(V1, V2, 0.9)])
        self.assertEqual(r.rank_points, 50.0)
        self.assertEqual(r.full_match_rank, 2)

    def test_full_match_rank4_25(self):
        rows = [single_row(WRONG, 0.97),
                single_row(("chr2", 222222, "A", "G"), 0.96),
                single_row(("chr3", 333333, "C", "A"), 0.95),
                comp_het_row(V1, V2, 0.9)]
        r = self.score(rows)
        self.assertEqual(r.rank_points, 25.0)

    def test_full_match_rank6_10(self):
        others = [("chr2", 222222, "A", "G"), ("chr3", 333333, "C", "A"),
                  ("chr4", 444444, "G", "T"), ("chr5", 555555, "T", "A"),
                  ("chr6", 666666, "A", "C")]
        rows = [single_row(v, 0.99 - i * 0.01) for i, v in enumerate(others)]
        rows.append(comp_het_row(V1, V2, 0.5))
        r = self.score(rows)
        self.assertEqual(r.rank_points, 10.0)
        self.assertEqual(r.full_match_rank, 6)


# ---------- comp-het 半分 ----------

class TestCompoundHetPartial(HarnessTestCase):
    def test_single_true_variant_alone_half_credit(self):
        r = self.score([single_row(V1, 0.9)])
        self.assertIsNone(r.full_match_rank)
        self.assertEqual(r.partial_match_rank, 1)
        self.assertEqual(r.rank_points, 50.0)  # 100 档的半分

    def test_true_variant_with_wrong_partner_half_credit(self):
        r = self.score([comp_het_row(V1, WRONG, 0.9)])
        self.assertEqual(r.partial_match_rank, 1)
        self.assertEqual(r.rank_points, 50.0)

    def test_partial_at_rank3_quarter_of_50(self):
        rows = [single_row(WRONG, 0.95),
                single_row(("chr2", 222222, "A", "G"), 0.92),
                single_row(V1, 0.9)]
        r = self.score(rows)
        self.assertEqual(r.rank_points, 25.0)  # 0.5 × 50(≤3 档)

    def test_full_match_beats_earlier_partial(self):
        """已有 full match 时不再找 partial —— full 的档位分优先。"""
        r = self.score([single_row(V1, 0.95), comp_het_row(V1, V2, 0.9)])
        self.assertEqual(r.full_match_rank, 2)
        self.assertEqual(r.rank_points, 50.0)
        self.assertIsNone(r.partial_match_rank)

    def test_split_pair_two_rows_fmax1_but_half_points(self):
        """拆成两行: F-max 可到 1.0，但 rank points 只有半分 —— 同行才满分。"""
        r = self.score([single_row(V1, 0.9), single_row(V2, 0.8)])
        self.assertIsNone(r.full_match_rank)
        self.assertEqual(r.rank_points, 50.0)
        self.assertAlmostEqual(r.f_max, 1.0)


# ---------- F-max 扫描 ----------

class TestFMax(HarnessTestCase):
    def test_perfect_fmax(self):
        r = self.score([comp_het_row(V1, V2, 1.0)])
        self.assertAlmostEqual(r.f_max, 1.0)
        self.assertEqual(r.n_predictions_at_f_max, 1)

    def test_fmax_penalized_by_false_positive(self):
        # t=0.95: 只有 WRONG → F=0；t=0.9: +{V1,V2} → P=2/3, R=1 → F=0.8
        r = self.score([single_row(WRONG, 0.95), comp_het_row(V1, V2, 0.9)])
        self.assertAlmostEqual(r.f_max, 0.8, places=6)

    def test_fmax_threshold_picks_best_cut(self):
        # t=0.9: {V1} → F=2/3；t=0.8: {V1,V2} → F=1.0 → 最佳阈值为 0.8
        r = self.score([single_row(V1, 0.9), single_row(V2, 0.8)])
        self.assertAlmostEqual(r.f_max, 1.0)
        self.assertEqual(r.f_max_threshold, 0.8)
        self.assertEqual(r.n_predictions_at_f_max, 2)

    def test_no_match_all_zero(self):
        r = self.score([single_row(WRONG, 0.9)])
        self.assertEqual(r.rank_points, 0.0)
        self.assertEqual(r.f_max, 0.0)
        self.assertIsNone(r.f_max_threshold)


# ---------- 排序与规范化 ----------

class TestSortingAndNormalization(HarnessTestCase):
    def test_rank_is_assigned_after_sorting(self):
        """官方按 epcr 降序排序后才定 rank —— 文件行序不重要，epcr 才是。"""
        r = self.score([comp_het_row(V1, V2, 0.5), single_row(WRONG, 0.9)])
        self.assertEqual(r.full_match_rank, 2)
        self.assertEqual(r.rank_points, 50.0)

    def test_ref_alt_case_insensitive(self):
        r = self.score([["PROBAND01", V1[0], V1[1], "t", "g",
                         V2[0], V2[1], "a", "c", 0.9, "primary", ""]])
        self.assertEqual(r.full_match_rank, 1)

    def test_chrom_prefix_sensitive_no_match(self):
        """'chr7' 与 '7' 不等价 —— 提交必须带 chr 前缀（官方模板与示例均为 chr 前缀）。

        单独提交改前缀的变异: 与答案无任何交集 → 0 分。
        (若与另一真变异配对，仍会因交集触发 partial 半分——见 TestCompoundHetPartial)
        """
        r = self.score([["PROBAND01", "7", V1[1], V1[2], V1[3],
                         "", "", "", "", 0.9, "primary", ""]])
        self.assertEqual(r.rank_points, 0.0)
        self.assertIsNone(r.full_match_rank)
        self.assertIsNone(r.partial_match_rank)


# ---------- 格式校验（preflight + 官方 loader） ----------

class TestPreflight(HarnessTestCase):
    def test_valid_submission_passes(self):
        _, code, out = self.run_harness([comp_het_row(V1, V2, 0.9)])
        self.assertEqual(code, 0)
        self.assertIn("Full match at rank 1", out)

    def test_reject_bad_proband(self):
        errs = scorer.preflight(write_csv(
            [["PROBAND02", *comp_het_row(V1, V2, 0.9)[1:]]],
            Path(self.tmp) / "bad.csv"))
        self.assertTrue(any("PROBAND01" in e for e in errs))

    def test_reject_epcr_out_of_range(self):
        for bad in ("0", "1.2", "abc"):
            errs = scorer.preflight(write_csv(
                [comp_het_row(V1, V2, bad)], Path(self.tmp) / "bad.csv"))
            self.assertTrue(any("epcr" in e for e in errs), bad)
        with self.assertRaises(ValueError):  # 官方 loader 同样拒绝
            scorer.ev.load_submission(write_csv(
                [comp_het_row(V1, V2, 0)], Path(self.tmp) / "o.csv"))

    def test_reject_bad_finding_type(self):
        errs = scorer.preflight(write_csv(
            [comp_het_row(V1, V2, 0.9, finding="candidate")],
            Path(self.tmp) / "bad.csv"))
        self.assertTrue(any("finding_type" in e for e in errs))
        with self.assertRaises(ValueError):
            scorer.ev.load_submission(write_csv(
                [comp_het_row(V1, V2, 0.9, finding="candidate")],
                Path(self.tmp) / "o.csv"))

    def test_reject_over_10_rows(self):
        rows = [comp_het_row(V1, V2, 0.99)] + [
            single_row(("chr%d" % i, i * 100000, "A", "G"), 0.9 - i * 0.05)
            for i in range(2, 12)]  # 共 11 行
        errs = scorer.preflight(write_csv(rows, Path(self.tmp) / "bad.csv"))
        self.assertTrue(any("10" in e for e in errs))
        with self.assertRaises(ValueError):
            scorer.ev.load_submission(write_csv(rows, Path(self.tmp) / "o.csv"))

    def test_reject_nonstandard_header(self):
        """本地比官方更严: 必须完整 12 列（官方 DictReader 容忍缺列）。"""
        errs = scorer.preflight(write_csv(
            [comp_het_row(V1, V2, 0.9)], Path(self.tmp) / "bad.csv",
            header=HEADER[:10]))
        self.assertTrue(any("表头" in e for e in errs))

    def test_reject_missing_chr_prefix(self):
        errs = scorer.preflight(write_csv(
            [["PROBAND01", "7", V1[1], V1[2], V1[3],
              V2[0], V2[1], V2[2], V2[3], 0.9, "primary", ""]],
            Path(self.tmp) / "noprefix.csv"))
        self.assertTrue(any("chr" in e for e in errs))

    def test_reject_incomplete_second_allele(self):
        errs = scorer.preflight(write_csv(
            [["PROBAND01", V1[0], V1[1], V1[2], V1[3],
              V2[0], "", "", "", 0.9, "primary", ""]],
            Path(self.tmp) / "half.csv"))
        self.assertTrue(any("第二等位" in e for e in errs))

    def test_unsorted_epcr_warns_but_passes(self):
        err_buf = io.StringIO()
        with contextlib.redirect_stderr(err_buf):
            errs = scorer.preflight(write_csv(
                [comp_het_row(V1, V2, 0.5), single_row(WRONG, 0.9)],
                Path(self.tmp) / "unsorted.csv"))
        self.assertEqual(errs, [])
        self.assertIn("警告", err_buf.getvalue())

    def test_reject_invalid_positions_before_official_loader(self):
        for column in (2, 6):
            for value in ("abc", "1.5", "0", "-5"):
                with self.subTest(column=column, value=value):
                    row = comp_het_row(V1, V2, 0.9)
                    row[column] = value
                    result, code, output = self.run_harness([row])
                    self.assertIsNone(result)
                    self.assertEqual(code, 1)
                    self.assertIn("正整数", output)

    def test_reject_missing_primary_alleles(self):
        for column in (3, 4):
            row = comp_het_row(V1, V2, 0.9)
            row[column] = " "
            self.assertEqual(self.run_harness([row])[1], 1)

    def test_reject_padded_header_that_dictreader_would_not_recognize(self):
        header = list(HEADER)
        header[0] = " proband_id "
        self.assertEqual(self.run_harness([comp_het_row(V1, V2, 0.9)], header)[1], 1)

    def test_reject_empty_fields_row_that_official_loader_would_read(self):
        self.assertEqual(self.run_harness([comp_het_row(V1, V2, 0.9), [""] * 12])[1], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
