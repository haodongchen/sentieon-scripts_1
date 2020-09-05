#!/usr/bin/env python

'''
Copyright (c) Sentieon Inc. All rights reserved.
  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
  POSSIBILITY OF SUCH DAMAGE.
'''

from __future__ import print_function

import argparse
import sys
import gzip

class Variant:
    def __init__(self):
        pass
        
        
def insert_by_QUAL(l, n):
    if len(l) == 0:
        return [n]
    nqual = float(n.split("\t")[5])
    lqual = [float(x.split("\t")[5]) for x in l]
    for i in range(len(l)):
        if lqual[i] < nqual:
            break
    else:
        i = len(l)
    # Inserting n in the list
    result = l[:i] + [n] + l[i:]
    return result


def triallelic_filter(block, args):
    output = []
    if args.mode == 1:
        args.N = 1
    if args.mode == 1 or args.mode == 2:
        output = block[:args.N]
    else:
        thresh = float(block[0].split("\t")[5]) * (100 - args.N) / 100
        for i in range(len(block)):
            if float(block[i].split("\t")[5]) < thresh:
                break
        else:
            i = len(block)
        output = block[:i]
    for line in output:
        cols = line.split("\t")
        filter_col = cols[6].split(";")
        filter_col.remove("triallelic_site")
        if len(filter_col) == 0:
            cols[6] = "PASS"
        else:
            cols[6] = ";".join(filter_col)
        print("\t".join(cols), end="")


def main():
    parser = argparse.ArgumentParser(description='Process triallelic sites.')
    parser.add_argument('-i', '--input', metavar='VCF',
                        help='Input VCF file name, required', required=True)
    parser.add_argument('-m', '--mode', metavar='MODE',
                        help='1) Keep the highest QUAL variant. '
                        '2) Keep top N variants. '
                        '3) Keep variants in top N%%. '
                        'Default: 1', type=int, default=1)
    parser.add_argument('-N', metavar='Parameter',
                        help='See --mode for more information', type=int)
    parser.add_argument('--ignore_non_pass',
                        help='Ignore and remove non-pass triallelic sites.',
                        action='store_true')
    args = parser.parse_args()
    if args.input.endswith("gz"):
        VCFfile = gzip.open(args.input, 'rt')
    else:
        VCFfile = open(args.input)
    block = []
    chrom = ""
    pos = ""
    for line in VCFfile:
        if line.startswith("#"):
            print(line, end="")
        else:
            cols = line.split("\t")
            if "triallelic_site" in cols[6].split(";"):
                if args.ignore_non_pass and cols[6] != "triallelic_site":
                    continue
                if block:
                    if cols[0] != chrom or int(cols[1]) != pos:
                        triallelic_filter(block, args)
                        block = [line]
                        chrom = cols[0]
                        pos = int(cols[1])
                    else:
                        block = insert_by_QUAL(block, line)
                else:
                    chrom = cols[0]
                    pos = int(cols[1])
                    block = [line]
            else:
                if block:
                    triallelic_filter(block, args)
                    block = []
                print(line, end="")
    if block:
        triallelic_filter(block, args)


if __name__ == '__main__':
    sys.exit(main())

# vim: ts=4 sw=4 expandtab
