import os
import unittest
from pipes import FileReader, FileParser, Producer, Sorter

__all__ = ['SorterTestCase']

SOURCE1 = os.path.join(os.path.dirname(__file__), '../data/source1.txt')
SOURCE2 = os.path.join(os.path.dirname(__file__), '../data/source2.txt')
SOURCE3 = os.path.join(os.path.dirname(__file__), '../data/source3.txt')
SOURCE1_SORTED = os.path.join(os.path.dirname(__file__), '../data/source1-sorted.txt')
SOURCE2_SORTED = os.path.join(os.path.dirname(__file__), '../data/source2-sorted.txt')
SOURCE3_SORTED = os.path.join(os.path.dirname(__file__), '../data/source3-sorted.txt')



class SorterTestCase(unittest.TestCase):
    def test_simple(self):
        iterables = [
            [0, 1, 3, 6, 8, 9],
            [0, 2, 3, 4],
            [3, 5, 6],
            [1, 2, 3, 7, 8, 10],
        ]

        result = Sorter(iterables)

        self.assertEqual(result, [
            [0, 1, 3, 6, 8, 9],
            [0, 2, 3, 4],
            [1, 2, 3, 7, 8, 10],
            [3, 5, 6],
        ])

    def test_records(self):
        keys = ('first', 'last', 'email', 'dob')

        def identity(obj, keys=keys):
            return [obj[key] for key in keys]

        fin1 = open(SOURCE1)
        keys1 = ('email', 'dob', 'facebook', 'first', 'last')
        reader1 = FileReader(fin1, skiplines=1)
        parser1 = FileParser(reader1)
        producer1 = Producer(parser1, keys1)
        sorter1 = Sorter(producer1, key=identity)

        self.assertEqual([tuple(next(sorter1)) for x in xrange(3)], [])

#        fin2 = open(SOURCE2)
#        keys2 = ('first', 'last', 'dob', 'email', 'twitter')
#        reader2 = FileReader(fin2, skiplines=1)
#        parser2 = FileParser(reader2)
#        producer2 = Producer(parser2, keys1)
#
#        fin3 = open(SOURCE3)
#        keys3 = ('dob', 'email', 'google+', 'first', 'last')
#        reader2 = FileReader(fin2, skiplines=1)
#        parser2 = FileParser(reader2)
#        producer2 = Producer(parser2, keys1)
#
#        self.assertEqual(len(results), 198)
#
#        self.assertEqual(results[:3], [
#            {'google+': '+Alec Fleming', 'last': 'Fleming', 'dob': '08/27/1985', 'twitter': '@alec_fleming', 'facebook': 'alec_fleming', 'email': 'natoque.penatibus@ligulaNullamenim.ca', 'first': 'Alec'},
#            {'google+': '+Alfonso Hardin', 'last': 'Hardin', 'dob': '01/13/1986', 'twitter': '@alfonso_hardin', 'facebook': 'alfonso_hardin', 'email': 'posuere.cubilia.Curae;@porttitor.org', 'first': 'Alfonso'},
#            {'google+': '+Ali Strong', 'last': 'Strong', 'dob': '01/05/1986', 'twitter': '@ali_strong', 'facebook': 'ali_strong', 'email': 'vitae.nibh@urna.ca', 'first': 'Ali'},
#        ])

if __name__ == '__main__':
    unittest.main()
