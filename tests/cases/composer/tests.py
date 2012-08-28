import os
import unittest
from pipes import compose

__all__ = ['ComposerTestCase']

SOURCE1 = os.path.join(os.path.dirname(__file__), '../../data/source1-sorted.txt')
SOURCE2 = os.path.join(os.path.dirname(__file__), '../../data/source2-sorted.txt')
SOURCE3 = os.path.join(os.path.dirname(__file__), '../../data/source3-sorted.txt')


class ComposerTestCase(unittest.TestCase):
    def test_simple(self):
        iterables = [
            [0, 1, 3, 6, 8, 9],
            [0, 2, 3, 4],
            [3, 5, 6],
            [1, 2, 3, 7, 8, 10],
        ]

        result = list(compose(iterables, identity=lambda x: x,
            merge=lambda x, y: x, relative=True))

        self.assertEqual(result, [
            (0, 0), (0, 1), (1, 2), (0, 3), (1, 4), (1, 5),
            (0, 6), (1, 7), (0, 8), (-1, 9), (1, 10)
        ])

    def test_records(self):
        keys = ('first', 'last', 'email', 'dob')

        def identity(obj, keys=keys):
            return '|'.join([obj[key] for key in keys])

        def s1():
            with open(SOURCE1) as fin:
                keys = ('email', 'dob', 'facebook', 'first', 'last')
                # Consume header
                fin.readline()
                for line in fin:
                    toks = line.strip().split('\t')
                    first, last = toks[0].split()
                    toks.append(first)
                    toks.append(last)
                    yield dict(zip(keys, toks[1:]))


        def s2():
            with open(SOURCE2) as fin:
                keys = ('first', 'last', 'dob', 'email', 'twitter')
                # Consume header
                fin.readline()
                for line in fin:
                    toks = line.strip().split('\t')
                    yield dict(zip(keys, toks))

        def s3():
            with open(SOURCE3) as fin:
                keys = ('dob', 'email', 'google+', 'first', 'last')
                # Consume header
                fin.readline()
                for line in fin:
                    toks = line.strip().split('\t')
                    last, first = toks[0].split(', ')
                    toks.append(first)
                    toks.append(last)
                    yield dict(zip(keys, toks[1:]))

        results = list(compose([s1(), s2(), s3()], identity=identity,
            merge=lambda x, y: x.update(y)))
        self.assertEqual(len(results), 198)

        self.assertEqual(results[:3], [
            {'google+': '+Alec Fleming', 'last': 'Fleming', 'dob': '08/27/1985', 'twitter': '@alec_fleming', 'facebook': 'alec_fleming', 'email': 'natoque.penatibus@ligulaNullamenim.ca', 'first': 'Alec'},
            {'google+': '+Alfonso Hardin', 'last': 'Hardin', 'dob': '01/13/1986', 'twitter': '@alfonso_hardin', 'facebook': 'alfonso_hardin', 'email': 'posuere.cubilia.Curae;@porttitor.org', 'first': 'Alfonso'},
            {'google+': '+Ali Strong', 'last': 'Strong', 'dob': '01/05/1986', 'twitter': '@ali_strong', 'facebook': 'ali_strong', 'email': 'vitae.nibh@urna.ca', 'first': 'Ali'},
        ])

if __name__ == '__main__':
    unittest.main()
