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
import argparse
import sys
import gzip
from operator import attrgetter


class Variant:
    __slots__ = ('chrom', 'pos', 'id', 'ref', 'alt', 'qual', 'filter',
                 'info', 'samples', 'line')

    def __init__(self, line):
        vals = line.rstrip().split('\t')
        if len(vals) < 10:
            raise ValueError('Variant has less than 10 columns.')
        vals[1] = int(vals[1])-1
        vals[4] = vals[4].split(',') if vals[4] != '.' else []
        vals[5] = float(vals[5]) if vals[5] != '.' else None
        vals[6] = vals[6].split(';') if vals[6] != '.' else []
        # Process INFO
        infoline = vals[7].split(";")
        vals[7] = {}
        for infoelem in infoline:
            if "=" not in infoelem:
                # Type=Flag
                infoelem += "=True"
            infoelem = infoelem.split("=")
            vals[7][infoelem[0]] = infoelem[1]
        fmts = vals[8].split(':')
        samples = []
        # Process FORMAT
        for val in vals[9:]:
            s = dict(zip(fmts, val.split(':')))
            samples.append(s)
        vals = vals[:8]
        vals.append(samples)
        vals.append(line.rstrip())
        for k, v in zip(self.__slots__, vals):
            setattr(self, k, v)

    def __str__(self):
        return self.line

    def __repr__(self):
        return self.line

    @property
    def alt_count(self):
        return int(self.samples[0]['AD'].split(",")[1])


def triallelic_filter(block, args):
    block.sort(reverse=True, key=attrgetter("qual", "alt_count"))
    output = []
    if args.mode == 1:
        output = block[:args.N]
    else:
        thresh = block[0].qual * (100 - args.N) / 100
        for i in range(len(block)):
            if block[i].qual < thresh:
                break
        else:
            i = len(block)
        output = block[:i]
    for var in output:
        cols = var.line.split("\t")
        filter_col = cols[6].split(";")
        filter_col.remove("triallelic_site")
        if len(filter_col) == 0:
            cols[6] = "PASS"
        else:
            cols[6] = ";".join(filter_col)
        print("\t".join(cols), end="\n")


def main():
    parser = argparse.ArgumentParser(description='Process triallelic sites.')
    parser.add_argument('-i', '--input', metavar='VCF',
                        help='Input VCF file name, required', required=True)
    parser.add_argument('-m', '--mode', metavar='MODE',
                        help='1) Keep top N variants. '
                        '2) Keep variants in top N%%. '
                        'Default: 1', type=int, default=1)
    parser.add_argument('-N', metavar='Parameter',
                        help='See --mode for more information. '
                        'Default: 1', type=int, default=1)
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
    pos = 0
    for line in VCFfile:
        if line.startswith("#"):
            print(line, end="")
        else:
            var = Variant(line)
            if "triallelic_site" in var.filter:
                if args.ignore_non_pass and len(var.filter) > 1:
                    continue
                if block:
                    if var.chrom != chrom or var.pos != pos:
                        triallelic_filter(block, args)
                        block = [Variant(line)]
                        chrom = var.chrom
                        pos = var.pos
                    else:
                        block.append(Variant(line))
                else:
                    chrom = var.chrom
                    pos = var.pos
                    block = [Variant(line)]
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
