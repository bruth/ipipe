from .iterbase import Iterable


class Reorder(Iterable):
    """Reorders each row of an iterable based on the keys.
    `iterable` rows must support `__getitem__` and be of instance that is
    inherently sortable, e.g. list, tuple, OrderedDict. By default, the same
    type will be used when outputing the record. Define an alternate by
    specifying `rowtype`.
    """
    def __init__(self, iterable, keys, fill=False, default=None, rowtype=None):
        self.iterable = iterable
        self.keys = keys
        self.positional = keys and type(keys[0]) is int or False
        self.fill = fill
        self.default = default
        self.rowtype = rowtype

    def _next(self, row):
        output = []
        for key in self.keys:
            if self.fill:
                try:
                    value = row[key]
                except KeyError:
                    value = self.default
            else:
                value = row[key]
            if self.positional:
                output.append(value)
            else:
                output.append((key, value))
        return self.rowtype(output)

    def next(self):
        row = next(self.iterable)
        if self.rowtype is None:
            self.rowtype = type(row)
        return self._next(row)
