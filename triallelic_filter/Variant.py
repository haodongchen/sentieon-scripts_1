class Variant:
    __slots__ = ('chrom', 'pos', 'id', 'ref', 'alt', 'qual', 'filter',
                 'info', 'samples', 'line')

    def __init__(self, line):
        vals = line.rstrip().split('\t')
        if len(vals) < 8:
            raise IndexError('Variant has less than 8 columns.')
        vals[1] = int(vals[1])-1
        vals[4] = vals[4].split(',') if vals[4] != '.' else []
        vals[5] = float(vals[5]) if vals[5] != '.' else None
        vals[6] = vals[6].split(';') if vals[6] != '.' else []
        if vals[7] != ".":
            # Process INFO
            infoline = vals[7].split(";")
            vals[7] = {}
            for infoelem in infoline:
                if "=" not in infoelem:
                    # Type=Flag
                    infoelem += "=True"
                infoelem = infoelem.split("=")
                vals[7][infoelem[0]] = infoelem[1]
        else:
            # no INFO
            vals[7] = {}
        samples = []
        if len(vals) > 9:
            # FORMATS and SAMPLES
            fmts = vals[8].split(':')
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
