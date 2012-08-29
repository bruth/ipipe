from collections import namedtuple
from .iterbase import Iterable


class Producer(Iterable):
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
        self.fields = fields

        # Create namedtuple class for this class
        name = '{}record'.format(self.__class__.__name__.lower())
        self.recordclass = namedtuple(name, fields)

    def next(self):
        return self.recordclass(*next(self.iterable))


class LineProducer(Iterable):
    "Delimited-line producer."
    def __init__(self, iterable, delimiter='\t'):
        self.iterable = iterable
        self.delimiter = delimiter

    def next(self):
        return self.delimiter.join(next(self.iterable)) + '\n'
