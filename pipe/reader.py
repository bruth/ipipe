class FileReader(object):
    "File reader that forces complete lines to be read."
    def __init__(self, source):
        self.source = source
        self.partial = None

    def __iter__(self):
        return self

    def read(self, size=-1, force=True):
        "Reads `size` bytes from the source."
        lines = self.source.read(size).splitlines()

        # If a partial line exists from the previous read
        if self.partial is not None:
            lines[0] = self.partial + lines[0]
            self.partial = None

        # If the last last is incomplete, it is stored as a partial for the
        # next read rather than reading over `size` bytes.
        last = lines.pop()
        if not last.endswith('\n'):
            # If there are no complete lines to process, nothing can be
            # returned. Check if a read should be forced to complete the line
            if not lines:
                if not force:
                    raise IOError('Cannot process an incomplete line.')
                lines.append(last + self.source.readline())
            else:
                self.partial = last
        return '\n'.join([self.parseline(line.rstrip('\n')) for line in lines])

    def readline(self, size=-1, force=True):
        "Reads `size bytes from the source up to a complete line."
        if force:
            line = self.source.readline()
        else:
            line = self.source.readline(size)
            if not line.endswith('\n'):
                raise IOError('Cannot process an incomplete line.')
        if self.partial is not None:
            line = self.partial + line
            self.partial = None
        if not line:
            return ''
        return self.parseline(line.rstrip('\n')) + '\n'

    def next(self):
        line = self.readline()
        if line == '':
            raise StopIteration
        return line


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
