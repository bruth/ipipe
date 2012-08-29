import unittest
from cStringIO import StringIO
from ipipe import Parser, FileParser

__all__ = ['ParserTestCase']


class ParserTestCase(unittest.TestCase):
    def test_base(self):
        parser = Parser((xrange(i * 5, (i+1) * 5) for i in xrange(5)))
        self.assertEqual([row for row in parser], [
            [0, 1, 2, 3, 4],
            [5, 6, 7, 8, 9],
            [10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19],
            [20, 21, 22, 23, 24],
        ])

    def test_parser(self):
        class Parser1(Parser):
            def parse_3(self, value):
                return value * 100

        parser  = Parser1((xrange(i * 5, (i+1) * 5) for i in xrange(5)))
        self.assertEqual([row for row in parser], [
            [0, 1, 2, 300, 4],
            [5, 6, 7, 800, 9],
            [10, 11, 12, 1300, 14],
            [15, 16, 17, 1800, 19],
            [20, 21, 22, 2300, 24],
        ])

    def test_file(self):
        buff = StringIO()
        buff.write('foo\tbar\tbaz\nbar\tbaz\tfoo\nbaz\tfoo\tbar')
        buff.seek(0)
        parser = FileParser(buff)
        self.assertEqual([row for row in parser], [
            ['foo', 'bar', 'baz'],
            ['bar', 'baz', 'foo'],
            ['baz', 'foo', 'bar'],
        ])



if __name__ == '__main__':
    unittest.main()
