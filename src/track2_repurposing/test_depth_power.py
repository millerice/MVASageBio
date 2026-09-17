#!/usr/bin/env python3
"""Synthetic-data tests for depth_power.py; contains no patient data."""

from __future__ import annotations

import random
import unittest

import depth_power as dp


class DepthPowerTests(unittest.TestCase):
    def setUp(self):
        self.rows = []
        for chrom in dp.AUTOS:
            for i in range(30):
                self.rows.append({
                    "chrom": chrom,
                    "start": i * 100_000,
                    "end": (i + 1) * 100_000,
                    "depth": 10.0 + (i % 10) * 0.2,
                    "gc": 0.30 + (i % 10) * 0.04,
                    "block": i // 10,
                })
        self.rows.sort(key=lambda r: (r["gc"], r["chrom"], r["start"]))

    def test_percentile_interpolates(self):
        self.assertEqual(dp.percentile([0, 10], 0.5), 5)

    def test_null_is_near_zero(self):
        self.assertAlmostEqual(dp.corrected_deviation(self.rows, "20", 0), 0, places=6)

    def test_pre_correction_spike_is_recovered(self):
        recovered = dp.corrected_deviation(self.rows, "20", 0.10)
        self.assertGreater(recovered, 0.09)
        self.assertLess(recovered, 0.101)

    def test_paired_recovery_removes_preexisting_offset(self):
        for row in self.rows:
            if row["chrom"] == "20":
                row["depth"] *= 1.02
        baseline = dp.corrected_deviation(self.rows, "20", 0)
        spiked = dp.corrected_deviation(self.rows, "20", 0.05)
        recovered = (((1 + spiked) / (1 + baseline)) - 1) / 0.05
        self.assertGreater(recovered, 0.99)
        self.assertLess(recovered, 1.01)

    def test_block_bootstrap_preserves_row_count(self):
        sampled = dp.block_bootstrap(self.rows, random.Random(7))
        self.assertEqual(len(sampled), len(self.rows))


if __name__ == "__main__":
    unittest.main(verbosity=2)
