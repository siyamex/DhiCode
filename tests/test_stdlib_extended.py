# tests/test_stdlib_extended.py - Tests for Network, Nakaiy, Prayer, and Thaana Math
import unittest
import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexer import Lexer
from parser import Parser
from evaluator import Evaluator, Environment, DhicodeString, DhicodeNumber, DhicodeList, DhicodeDict

def run_dhi(code: str) -> tuple:
    outputs = []
    def record_output(val):
        outputs.append(str(val))

    lexer = Lexer(code)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert not parser.errors, f"Parser errors: {parser.errors}"

    evaluator = Evaluator(output_callback=record_output)
    env = Environment()
    result = evaluator.eval(program, env)
    return result, outputs, env

class TestExtendedStdLib(unittest.TestCase):
    def test_json_and_network(self):
        code = '''
        ގެނޭ "ނެޓްވޯކް"
        ކަނޑައަޅާ މީހާ = {"ނަން": "ޢަލީ", "އުމުރު": 25}
        ކަނޑައަޅާ ޖޭސަން_ލިޔުން = ޖޭސަން_ހަދާ(މީހާ)
        ކަނޑައަޅާ އަލުން = ޖޭސަން_ކިޔާ(ޖޭސަން_ލިޔުން)
        ދައްކާ އަލުން["ނަން"]
        '''
        res, outputs, env = run_dhi(code)
        self.assertIn("ޢަލީ", outputs)

    def test_nakaiy_calendar(self):
        code = '''
        ގެނޭ "ނަކަތް"
        ކަނޑައަޅާ މިއަދު = މިއަދުގެ_ނަކަތް()
        ދައްކާ މިއަދު["މޫސުން"]

        // Look up specific Nakaiy: May 10 -> Kethi (ކެތި)
        ކަނޑައަޅާ ކެތި = ނަކަތް_ހޯދާ(5, 10)
        ދައްކާ ކެތި["ނަން"]
        '''
        res, outputs, env = run_dhi(code)
        self.assertTrue(any("ހުޅަނގު" in o or "އިރުވައި" in o for o in outputs))
        self.assertIn("ކެތި", outputs)

    def test_prayer_times(self):
        code = '''
        ގެނޭ "ނަމާދު"
        ކަނޑައަޅާ ވަގުތު = މިއަދުގެ_ވަގުތު("މާލެ")
        ދައްކާ ވަގުތު["މެންދުރު"]
        '''
        res, outputs, env = run_dhi(code)
        self.assertTrue(len(outputs) > 0)
        # Should be a valid time format like "12:xx"
        self.assertTrue(":" in outputs[0])

    def test_thaana_number_to_words(self):
        code = '''
        ގެނޭ "ތާނަ_ހިސާބު"
        ދައްކާ އަދަދު_ބަހަށް(0)
        ދައްކާ އަދަދު_ބަހަށް(7)
        ދައްކާ އަދަދު_ބަހަށް(25)
        ދައްކާ އަދަދު_ބަހަށް(125)
        '''
        res, outputs, env = run_dhi(code)
        self.assertIn("ސުމެއް", outputs)
        self.assertIn("ހަތެއް", outputs)
        self.assertIn("ފަންސަވީސް", outputs)
        self.assertIn("ސަތޭކަ ފަންސަވީސް", outputs)

    def test_thaana_collation(self):
        code = '''
        ގެނޭ "ތާނަ_ހިސާބު"
        ކަނޑައަޅާ ބަސްތައް = ["ރަށް", "ހަނދު", "ނަން", "ށީ"]
        ކަނޑައަޅާ ތަރުތީބު = ތާނަ_ތަރުތީބު(ބަސްތައް)
        ދައްކާ ތަރުތީބު[0]
        ދައްކާ ތަރުތީބު[1]
        ދައްކާ ތަރުތީބު[2]
        ދައްކާ ތަރުތީބު[3]
        '''
        # Alphabet: ހ, ށ, ނ, ރ
        res, outputs, env = run_dhi(code)
        self.assertEqual(outputs[0], "ހަނދު")
        self.assertEqual(outputs[1], "ށީ")
        self.assertEqual(outputs[2], "ނަން")
        self.assertEqual(outputs[3], "ރަށް")

if __name__ == "__main__":
    unittest.main()
