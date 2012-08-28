from collections import namedtuple


class Producer(object):
    """An iterator class that wraps an iterable. Each `line` will be mapped
    converted to a record object for downstream processing.

    `fields` is an array of field names that are valid variable
    names as keys and their position relative to the row.

        fields = [('id', 0), ('name', 3), ('email', 1)]

    A list of just the field names can be defined. This assumes data is
    in the same order:

        fields = ['id', 'name', 'email']
    """
    def __init__(self, iterable, fields):
        self.iterable = iterable
        if not isinstance(fields[0], (list, tuple)):
            fields = [(f, i) for i, f in enumerate(fields)]
        self.fields = fields

        # Create namedtuple class for this class
        name = '{}record'.format(self.__class__.__name__.lower())
        self.recordclass = namedtuple(name, [f for f, i in fields])

    def next(self):
        return self.emit(next(self.iterable))

    def emit(self, row):
        return self.recordclass(*[row[i] for f, i in self.fields])
