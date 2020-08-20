# Triallelic Filter
Filter triallelic sites to keep the high QUAL variants.

### Usage ###
```
usage: triallelic_filter.py [-h] -i VCF -m MODE [-N Parameter]
                            [--ignore_non_pass]

Process triallelic sites.

optional arguments:
  -h, --help            show this help message and exit
  -i VCF, --input VCF   Input VCF file name, required
  -m MODE, --mode MODE  1) Keep the highest QUAL variant. 2) Keep the top N
                        variants. 3) Keep the variants whose QUAL is more than
                        N% of the highest.
  -N Parameter          See --mode for more information
  --ignore_non_pass     Determines whether to skip non-pass variants.
```
