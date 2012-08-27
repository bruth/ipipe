class Sorter(object):
    def __init__(self, iterable, key=None):
        self.iterable = iterable
        self.key = key
        self.sorted = None

    def __iter__(self):
        return self

    def next(self):
        if self.sorted is None:
            # Wrap in generator expression to consume once
            self.sorted = (row for row in sorted(self.iterable, key=self.key))
        return next(self.sorted)
