import unittest
from Variant import Variant


class VariantTest(unittest.TestCase):
    def test_init(self):
        line = "chr22\t16059753\trs114433833\tA\tT\t21.77\t.\tAC=2;AF=1.000;" \
          "AN=2;DB;DP=3;ExcessHet=3.0103;FS=0.000;MLEAC=2;MLEAF=1.000;MQ=60" \
          ";QD=10.88;SOR=0.693\tGT:AD:DP:GQ:PL\t1/1:0,2:2:6:49,6,0\n"
        var = Variant(line)
        attr = ['chrom', 'pos', 'id', 'ref', 'alt', 'qual', 'filter']
        val = ['chr22', 16059752, 'rs114433833', 'A', ['T'], 21.77, []]
        for k, v in zip(attr, val):
            assert getattr(var, k) == v
        kw_info = ['AC', 'AF', 'AN', 'DB', 'DP', 'ExcessHet', 'FS', 'MLEAC',
              'MLEAF', 'MQ', 'QD', 'SOR']
        val_info = ['2', '1.000', '2', 'True', '3', '3.0103', '0.000', '2',
               '1.000', '60', '10.88', '0.693']
        for k, v in zip(kw_info, val_info):
            assert var.info[k] == v
        kw_fmts = ['GT', 'AD', 'DP', 'GQ', 'PL']
        val_fmts = ['1/1', '0,2', '2', '6', '49,6,0']
        for k, v in zip(kw_fmts, val_fmts):
            assert var.samples[0][k] == v


if __name__ == "__main__":
    unittest.main()
