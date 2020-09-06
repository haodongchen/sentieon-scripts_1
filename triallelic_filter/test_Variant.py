import unittest
from Variant import Variant


class VariantTest(unittest.TestCase):
    def test_init(self):
        line = "chr22\t16059753\trs114433833\tA\tT\t21.77\t.\tAC=2;AF=1.000;" \
          "AN=2;DB;DP=3;ExcessHet=3.0103;FS=0.000;MLEAC=2;MLEAF=1.000;MQ=60" \
          "\tGT:AD:DP:GQ:PL\t0/1:0,2:2:6:49,6,0\t0/0:5,0:5:6:0,1,40\n"
        var = Variant(line)
        attr = ['chrom', 'pos', 'id', 'ref', 'alt', 'qual', 'filter']
        val = ['chr22', 16059752, 'rs114433833', 'A', ['T'], 21.77, []]
        for k, v in zip(attr, val):
            assert getattr(var, k) == v
        kw_info = ['AC', 'AF', 'AN', 'DB', 'DP', 'ExcessHet', 'FS', 'MLEAC',
                   'MLEAF', 'MQ']
        val_info = ['2', '1.000', '2', 'True', '3', '3.0103', '0.000', '2',
                    '1.000', '60']
        for k, v in zip(kw_info, val_info):
            assert var.info[k] == v
        kw_fmts = ['GT', 'AD', 'DP', 'GQ', 'PL']
        val_fmts1 = ['0/1', '0,2', '2', '6', '49,6,0']
        val_fmts2 = ['0/0', '5,0', '5', '6', '0,1,40']
        for k, v1, v2 in zip(kw_fmts, val_fmts1, val_fmts2):
            assert var.samples[0][k] == v1
            assert var.samples[1][k] == v2
        assert var.line == line.rstrip()

    def test_init_too_short(self):
        line = "chr22\t16059753\trs114433833\tA\tT\t21.77\t.\n"
        with self.assertRaises(IndexError):
            var = Variant(line)


if __name__ == "__main__":
    unittest.main()
