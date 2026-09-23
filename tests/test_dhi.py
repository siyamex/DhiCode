# tests/test_dhi.py
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lexer import Lexer
from parser import Parser
from evaluator import Evaluator, Environment, DhicodeNumber, DhicodeString, DhicodeBoolean

class TestDhiCode(unittest.TestCase):
    def eval_code(self, code: str):
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        self.assertEqual(parser.errors, [], f"Parser errors: {parser.errors}")
        evaluator = Evaluator()
        env = Environment()
        return evaluator.eval(program, env)

    def test_arithmetic(self):
        res = self.eval_code("5 + 5 * 2 - 3")
        self.assertIsInstance(res, DhicodeNumber)
        self.assertEqual(res.value, 12)

    def test_variable_assignment(self):
        code = """
        ކަނޑައަޅާ އަގު1 = 20
        ކަނޑައަޅާ އަގު2 = 30
        އަގު1 + އަގު2
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeNumber)
        self.assertEqual(res.value, 50)

    def test_strings_concatenation(self):
        code = """
        ކަނޑައަޅާ ނަން = "ދިވެހި"
        ނަން + " ރާއްޖެ"
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeString)
        self.assertEqual(res.value, "ދިވެހި ރާއްޖެ")

    def test_if_else(self):
        code = """
        ކަނޑައަޅާ އުމުރު = 15
        ކަނޑައަޅާ ޖަވާބު = "ކުޑަކުއްޖެއް"
        ނަމަ އުމުރު > 18
            ކަނޑައަޅާ ޖަވާބު = "ބޮޑު މީހެއް"
        ނޫންނަމަ
            ކަނޑައަޅާ ޖަވާބު = "ޅަފުރާ"
        ނިމުނީ
        ޖަވާބު
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeString)
        self.assertEqual(res.value, "ޅަފުރާ")

    def test_while_loop(self):
        code = """
        ކަނޑައަޅާ ޖުމްލަ = 0
        ކަނޑައަޅާ ގުނާ = 1
        ހިނދު ގުނާ <= 5
            ކަނޑައަޅާ ޖުމްލަ = ޖުމްލަ + ގުނާ
            ކަނޑައަޅާ ގުނާ = ގުނާ + 1
        ނިމުނީ
        ޖުމްލަ
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeNumber)
        self.assertEqual(res.value, 15)

    def test_function_and_recursion(self):
        code = """
        ވަޒީފާ ފެކްޓޯރިއަލް(އަދަދު)
            ނަމަ އަދަދު <= 1
                ފޮނުވާ 1
            ނިމުނީ
            ފޮނުވާ އަދަދު * ފެކްޓޯރިއަލް(އަދަދު - 1)
        ނިމުނީ

        ފެކްޓޯރިއަލް(5)
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeNumber)
        self.assertEqual(res.value, 120)

    def test_boolean_and_logical(self):
        code = """
        ކަނޑައަޅާ ތެދު = އާން
        ކަނޑައަޅާ ދޮގު = ނޫން
        ތެދު އަދި ދޮގު
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeBoolean)
        self.assertEqual(res.value, False)

        code_or = """
        އާން ނުވަތަ ނޫން
        """
        res_or = self.eval_code(code_or)
        self.assertIsInstance(res_or, DhicodeBoolean)
        self.assertEqual(res_or.value, True)

if __name__ == "__main__":
    unittest.main()
