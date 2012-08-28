class FileReader(object):
    "File reader that forces complete lines to be read."
    def __init__(self, iterable, skiplines=0):
        self.iterable = iterable
        self.skiplines = skiplines
        self.skipped = None

    def __iter__(self):
        return self

    def next(self):
        if self.skipped is None:
            self.skipped = []
            for _ in xrange(self.skiplines):
                self.skipped.append(next(self.iterable))
        return next(self.iterable)


class CursorReader(object):
    "Reader that wraps a database cursor."
    def __init__(self, cursor, batchsize=100):
        self.cursor = cursor
        self.batchsize = batchsize
        self.batch = None
        self._iter = None

    def __iter__(self):
        return self

    def _result_iter(self):
        while True:
            if not self.batch:
                self.batch = self.cursor.fetchmany(self.batchsize)
                if not self.batch:
                    raise StopIteration
            for row in self.batch:
                yield row

    def next(self):
        if self._iter is None:
            self._iter = self._result_iter()
        return next(self._iter)
