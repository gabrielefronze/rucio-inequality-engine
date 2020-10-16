import unittest
from inequalityengine import OP, clear_double_spaces, translate, inequality_engine

class TestTranslate(unittest.TestCase):

    def test_Translate(self):
        for translated_op in OP.keys():
            op_list = OP[translated_op]
            for op in op_list:
                string = 'A'+op+'B'
                control = 'A'+translated_op+'B'
                self.assertEqual(translate(string), control)


class TestClearDoubleSpaces(unittest.TestCase):

    def test_ClearDoubleSpaces(self):
        string = 'test string        contains    multiple           repeated spaces      '
        control = 'test string contains multiple repeated spaces'
        self.assertEqual(clear_double_spaces(string), control)

class TestInequalityEngine(unittest.TestCase):

    def test_AndGroups(self):
        string = "True"
        self.assertTrue(inequality_engine(string).run())

        string = "True, True"
        self.assertTrue(inequality_engine(string).run())

        string = "True, False"
        self.assertFalse(inequality_engine(string).run())

        string = "6 >= 6"
        self.assertTrue(inequality_engine(string).run())

        string = "5 > 2, 1200-10 < 1200"
        self.assertTrue(inequality_engine(string).run())

        string = "5 == 5, 1200-10 > 1200"
        self.assertFalse(inequality_engine(string).run())

        string = "5 = 5, 1200-10 > 1200"
        self.assertFalse(inequality_engine(string).run())

    def test_OrGroups(self):
        string = "True; True"
        self.assertTrue(inequality_engine(string).run())

        string = "True; False"
        self.assertTrue(inequality_engine(string).run())

        string = "False; False"
        self.assertFalse(inequality_engine(string).run())

        string = "100 >= 42; False"
        self.assertTrue(inequality_engine(string).run())

        string = "100 < 42; False"
        self.assertFalse(inequality_engine(string).run())

        string = "100 < 42; False; 7 > 8; 2**10 == 1024"
        self.assertTrue(inequality_engine(string).run())

    def test_RangeConversion(self):
        string = "2 < 10 < 100"
        self.assertTrue(inequality_engine(string).run())

        string = "20 > 10 < 100"
        self.assertTrue(inequality_engine(string).run())

        string = "2 < 100 <= 100"
        self.assertTrue(inequality_engine(string).run())

        string = "2 < 100 < 100"
        self.assertFalse(inequality_engine(string).run())

        string = "20 > 10 > 100"
        self.assertFalse(inequality_engine(string).run())

        string = "20 >= 20 >= 100"
        self.assertFalse(inequality_engine(string).run())

    def test_InequalityEngine(self):
        string = "True, True; True"
        self.assertTrue(inequality_engine(string).run())

        string = "True, False; True"
        self.assertTrue(inequality_engine(string).run())

        string = "False, False; True"
        self.assertTrue(inequality_engine(string).run())

        string = "False, False; False"
        self.assertFalse(inequality_engine(string).run())

if __name__ == '__main__':
    unittest.main()