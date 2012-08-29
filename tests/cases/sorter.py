import os
import unittest
from ipipe import FileReader, FileParser, Producer, Sorter

__all__ = ['SorterTestCase']

SOURCE1 = os.path.join(os.path.dirname(__file__), '../data/source1.txt')
SOURCE2 = os.path.join(os.path.dirname(__file__), '../data/source2.txt')
SOURCE3 = os.path.join(os.path.dirname(__file__), '../data/source3.txt')


class SorterTestCase(unittest.TestCase):
    def test_simple(self):
        iterables = [
            [0, 1, 3, 6, 8, 9],
            [0, 2, 3, 4],
            [3, 5, 6],
            [1, 2, 3, 7, 8, 10],
        ]

        result = Sorter(iterables)

        self.assertEqual(list(result), [
            [0, 1, 3, 6, 8, 9],
            [0, 2, 3, 4],
            [1, 2, 3, 7, 8, 10],
            [3, 5, 6],
        ])

    def test_records(self):
        def identity(obj):
            return obj.first, obj.last, obj.email, obj.dob

        class Parser1(FileParser):
            def parse_0(self, value):
                return value.split()

        fin = open(SOURCE1)
        reader = FileReader(fin, skiplines=1)
        parser = Parser1(reader)

        keys = ('first', 'last', 'email', 'dob', 'facebook')
        producer = Producer(parser, keys)
        sorter = Sorter(producer, key=identity)

        self.assertEqual([tuple(next(sorter)) for x in xrange(3)], [
            ('Alec', 'Fleming', 'natoque.penatibus@ligulaNullamenim.ca', '08/27/1985', 'alec_fleming'),
            ('Alfonso', 'Hardin', 'posuere.cubilia.Curae;@porttitor.org', '01/13/1986', 'alfonso_hardin'),
            ('Ali', 'Strong', 'vitae.nibh@urna.ca', '01/05/1986', 'ali_strong'),
        ])

if __name__ == '__main__':
    unittest.main()
