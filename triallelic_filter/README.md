# Triallelic Filter
Filter triallelic sites to keep the high QUAL variants.

### Usage ###
```
usage: triallelic_filter.py [-h] -i VCF [-m MODE] [-N Parameter]
                            [--ignore_non_pass]

Process triallelic sites.

optional arguments:
  -h, --help            show this help message and exit
  -i VCF, --input VCF   Input VCF file name, required
  -m MODE, --mode MODE  1) Keep the highest QUAL variant. 2) Keep the top N
                        variants. 3) Keep the variants whose QUAL is more than
                        N% of the highest. Default: 1
  -N Parameter          See --mode for more information
  --ignore_non_pass     Determines whether to skip non-pass variants.
```
## Examples
Input:
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Tumor Normal
22	19679446	.	C	CA	100	triallelic_site	.	GT	0/1	0/0
22	19679446	.	C	CAA	1013	triallelic_site	.	GT	0/1	0/0
22	19679446	.	C	CAAA	5000	triallelic_site;germline_risk	.	GT	0/1	0/0
```
### Mode 1 (Default) ###
Keep the triallelic site with the highest QUAL.
```
$ python triallelic_filter.py -i input.vcf
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Tumor Normal
22	19679446	.	C	CAAA	5000	germline_risk	.	GT	0/1	0/0
```
Keep the triallelic site with the highest QUAL but ignore sites with FILTER other than `triallelic_site`.
```
$ python triallelic_filter.py -i input.vcf --ignore_non_pass
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Tumor Normal
22	19679446	.	C	CAA	1013	PASS	.	GT	0/1	0/0
```

