# tests/test_dhi.py
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lexer import Lexer
from parser import Parser
from evaluator import Evaluator, Environment, DhicodeNumber, DhicodeString, DhicodeBoolean, DhicodeList, DhicodeDict

class TestDhiCode(unittest.TestCase):
    def eval_code(self, code: str):
        lexer = Lexer(code)
        parser = Parser(lexer)
        program = parser.parse_program()
        self.assertEqual(parser.errors, [], f"Parser errors: {parser.errors}")
        evaluator = Evaluator(base_path=os.path.abspath("."))
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

    def test_boolean_and_logic(self):
        code = "އާން އަދި ނޫން"
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeBoolean)
        self.assertEqual(res.value, False)

        code_or = "އާން ނުވަތަ ނޫން"
        res_or = self.eval_code(code_or)
        self.assertIsInstance(res_or, DhicodeBoolean)
        self.assertEqual(res_or.value, True)

    def test_lists_and_indexing(self):
        code = """
        ކަނޑައަޅާ މޭވާތައް = ["އަނބު", "ކެޔޮ", "ޖަންބުރޯލު"]
        މޭވާތައް[1]
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeString)
        self.assertEqual(res.value, "ކެޔޮ")

        # Negative indexing and append
        code2 = """
        ކަނޑައަޅާ ލިސްޓު = [10, 20]
        އަޅާ(ލިސްޓު, 30)
        ލިސްޓު[-1]
        """
        res2 = self.eval_code(code2)
        self.assertIsInstance(res2, DhicodeNumber)
        self.assertEqual(res2.value, 30)

    def test_dictionaries(self):
        code = """
        ކަނޑައަޅާ މީހާ = {"ނަން": "ޙަސަން", "އުމުރު": 30}
        މީހާ["ނަން"]
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeString)
        self.assertEqual(res.value, "ޙަސަން")

    def test_for_in_loop(self):
        code = """
        ކަނޑައަޅާ ޖުމްލަ = 0
        ކޮންމެ އަދަދު ތެރޭގައި [1, 2, 3, 4]
            ކަނޑައަޅާ ޖުމްލަ = ޖުމްލަ + އަދަދު
        ނިމުނީ
        ޖުމްލަ
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeNumber)
        self.assertEqual(res.value, 10)

    def test_math_module_import(self):
        code = """
        ގެނޭ "ހިސާބު"
        ކަނޑައަޅާ ޖ = ޖަޒުރު(25)
        ކަނޑައަޅާ ބ = ބާރު(2, 4)
        ޖ + ބ
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeNumber)
        self.assertEqual(res.value, 21)

    def test_try_catch_recovery(self):
        code = """
        ކަނޑައަޅާ ހާލަތު = "ހަމަޖެހިފައި"
        މަސައްކަތްކުރޭ
            ކަނޑައަޅާ ކ = 10 / 0
        ކުށެއް_ފެނިއްޖެނަމަ މައްސަލަ
            ކަނޑައަޅާ ހާލަތު = "ކުށެއް ސަލާމަތްކުރެވިއްޖެ"
        ނިމުނީ
        ހާލަތު
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeString)
        self.assertEqual(res.value, "ކުށެއް ސަލާމަތްކުރެވިއްޖެ")

    def test_throw_statement(self):
        code = """
        ކަނޑައަޅާ ޖަވާބު = ""
        މަސައްކަތްކުރޭ
            އުކާލާ "ޚާއްޞަ ކުށެއް"
        ކުށެއް_ފެނިއްޖެނަމަ ސަބަބު
            ކަނޑައަޅާ ޖަވާބު = ސަބަބު
        ނިމުނީ
        ޖަވާބު
        """
        res = self.eval_code(code)
        self.assertIsInstance(res, DhicodeString)
        self.assertEqual(res.value, "ޚާއްޞަ ކުށެއް")

if __name__ == "__main__":
    unittest.main()
