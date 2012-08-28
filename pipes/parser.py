noop = lambda x: x


class Parser(object):
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return self

    def next(self):
        return self.parse(next(self.iterable))

    # Base parser assume `row` is already a list or tuple
    def parse(self, row):
        output = []
        for i, value in enumerate(row):
            parsed = getattr(self, 'parse_{}'.format(i), noop)(value)
            if isinstance(parsed, (list, tuple)):
                output.extend(parsed)
            else:
                output.append(parsed)
        return output


class FileParser(Parser):
    def __init__(self, iterable, delimiter='\t'):
        self.iterable = iterable
        self.delimiter = delimiter

    def parse(self, line):
        row = line.strip().split(self.delimiter)
        return super(FileParser, self).parse(row)
