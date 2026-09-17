import unittest
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from summarize import category


class SummaryTests(unittest.TestCase):
    def result(self, ref, alt, conflict=0):
        return category(dict(ref_fragments=ref, alt_fragments=alt, mate_conflicts=conflict))

    def test_counts_insufficient_even_when_balanced(self):
        d = self.result(4, 4)
        self.assertEqual(d['reason_categories'], ['ALT_SUPPORT_BELOW_THRESHOLD'])

    def test_conflict_is_separate_from_original_threshold(self):
        d = self.result(5, 5, 1)
        self.assertTrue(d['original_support_threshold_pass'])
        self.assertEqual(d['extended_support_status'], 'not_pass')

    def test_balance_boundary_is_exact(self):
        self.assertTrue(self.result(14, 6)['original_support_threshold_pass'])
        self.assertFalse(self.result(15, 6)['original_support_threshold_pass'])

    def test_empty_is_uninformative_not_balanced(self):
        self.assertIn('NO_USABLE_REF_ALT_SUPPORT', self.result(0, 0)['reason_categories'])

    @unittest.skipUnless(shutil.which('samtools'), 'samtools required for synthetic integration test')
    def test_real_bam_duplicate_filtering_and_categorical_export(self):
        task = Path(__file__).resolve().parent
        validator = task.parent / 'q1_full_reference_recheck/validate_bam.py'
        if not validator.is_file():
            self.skipTest('frozen sibling validator is required')
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            ref = work / 'synthetic.fa'
            ref.write_text('>synthetic\n' + 'A' * 600 + '\n')
            subprocess.run(['samtools', 'faidx', str(ref)], check=True)
            targets = work / 'targets.tsv'
            with targets.open('w', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                writer.writerow(['label', 'contig', 'position', 'ref', 'alt'])
                for i, pos in enumerate((150, 350)):
                    writer.writerow([f'private_label_{i}', 'synthetic', pos, 'A', 'C'])
            sam = work / 'reads.sam'
            lines = ['@HD\tVN:1.6\tSO:coordinate', '@SQ\tSN:synthetic\tLN:600']
            for locus, pos in enumerate((150, 350)):
                for i in range(14):
                    base = 'A' if i < 8 else 'C'
                    # For the second synthetic candidate only, two ALT reads are duplicates.
                    flag = 1024 if locus == 1 and i >= 12 else 0
                    lines.append('\t'.join(map(str, [f'read_{locus}_{i}', flag, 'synthetic', pos, 60, '1M', '*', 0, 0, base, 'I'])))
            sam.write_text('\n'.join(lines) + '\n')
            before, after = work / 'before.bam', work / 'after.bam'
            subprocess.run(['samtools', 'view', '-b', '-o', str(before), str(sam)], check=True)
            subprocess.run(['samtools', 'view', '-b', '-F', '1024', '-o', str(after), str(before)], check=True)
            for bam in (before, after):
                subprocess.run(['samtools', 'index', str(bam)], check=True)
            subprocess.run([sys.executable, '-B', str(task / 'summarize.py'),
                            '--validator', str(validator), '--targets', str(targets),
                            '--reference', str(ref), '--l001-before', str(before), '--l001-after', str(after),
                            '--l002-before', str(before), '--l002-after', str(after), '--output', str(work)], check=True)
            text = (work / 'return/q1_l002_safe_summary.json').read_text()
            result = json.loads(text)
            for lane in ('L001', 'L002'):
                self.assertEqual(result['stages'][lane + '_before']['candidates'][1]['extended_support_status'], 'pass')
                self.assertEqual(result['stages'][lane + '_after']['candidates'][1]['reason_categories'], ['ALT_SUPPORT_BELOW_THRESHOLD'])
                self.assertEqual(result['stages'][lane + '_after']['candidates'][0]['extended_support_status'], 'pass')
            for private_text in ('private_label_', 'read_0_', 'ref_fragments', 'alt_fragments', 'synthetic'):
                self.assertNotIn(private_text, text)


if __name__ == '__main__':
    unittest.main()
