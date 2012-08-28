import itertools


class Iterable(object):
    "Iterable wrapper for pipeline components."
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return self

    def __getitem__(self, idx):
        try:
            return next(itertools.islice(self, idx, idx + 1))
        except TypeError:
            return list(itertools.islice(self, idx.start, idx.stop, idx.step))

    def next(self):
        return next(self.iterable)
