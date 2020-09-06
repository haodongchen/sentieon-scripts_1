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
  -m MODE, --mode MODE  1) Keep top N variants. 2) Keep variants in top N%.
                        Default: 1
  -N Parameter          See --mode for more information. Default: 1
  --ignore_non_pass     Ignore and remove non-pass triallelic sites.
```
## Examples
Input:
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Tumor Normal
22	19679446	.	C	CA	100	triallelic_site	.	GT:AD	0/1:2,5	0/0:10,0
22	19679446	.	C	CAA	1013	triallelic_site	.	GT:AD	0/1:2,6	0/0:8,1
22	19679446	.	C	CAAA	5000	triallelic_site;germline_risk	.	GT:AD	0/1:7,23	0/0:12,0
```
### Mode 1 (Keep the top triallelic site ranked by QUAL and AD. Default) ###
Keep the top one triallelic site.
```
$ python triallelic_filter.py -i input.vcf
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Tumor Normal
22	19679446	.	C	CAAA	5000	germline_risk	.	GT:AD	0/1:7,23	0/0:12,0
```
Keep the top two triallelic sites.
```
$ python triallelic_filter.py -i input.vcf -N 2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Tumor Normal
22	19679446	.	C	CAA	1013	PASS	.	GT:AD	0/1:2,6	0/0:8,1
22	19679446	.	C	CAAA	5000	germline_risk	.	GT:AD	0/1:7,23	0/0:12,0
```
Keep the triallelic site with the highest QUAL but ignore sites with FILTER other than `triallelic_site`.
```
$ python triallelic_filter.py -i input.vcf --ignore_non_pass
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Tumor Normal
22	19679446	.	C	CAA	1013	PASS	.	GT:AD	0/1:2,6	0/0:8,1
```

