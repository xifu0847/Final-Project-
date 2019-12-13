import unittest
import os
import process


class TestProcessLibrary(unittest.TestCase):
    '''
    Unit test for process.py
    '''
    def setUp(self):
        pass

    def test_parse_input(self):
        header, gene = process.parse_input('merged_gene_counts.txt')
        self.assertEqual(header, [
            'Geneid', 'gene_name', 'Fast_A3_1Aligned.sortedByCoord.out.bam',
            'OF_A7_1Aligned.sortedByCoord.out.bam',
            's_3DPF_C4_1Aligned.sortedByCoord.out.bam',
            'OFF_A10_1Aligned.sortedByCoord.out.bam',
            'Fast_A6_1Aligned.sortedByCoord.out.bam',
            'OFF_A13_1Aligned.sortedByCoord.out.bam',
            'OF_A8_1Aligned.sortedByCoord.out.bam',
            's_3DPF_A4_1Aligned.sortedByCoord.out.bam'
        ])
        self.assertNotEqual(len(gene), 0)

    def test_NCBI_url(self):
        uid, name, description, summary, organ = process.NCBI_url('GMPPA')
        # The following result is captured from
        # https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=685&retmode=json
        self.assertEqual(uid, 685)
        self.assertEqual(name, 'GMPPA')
        self.assertEqual(description, 'betacellulin')
        self.assertEqual(organ, 'Homo sapiens')


if __name__ == '__main__':
    unittest.main()
