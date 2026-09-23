# tests/test_core_extensions.py
import unittest
from lexer import Lexer
from parser import Parser
from evaluator import Evaluator, Environment, DhicodeNumber, DhicodeString, DhicodeBoolean, DhicodeNull, DhicodeError

def run_dhi(code: str, output_list=None):
    if output_list is None:
        output_list = []
    evaluator = Evaluator(output_callback=output_list.append)
    lexer = Lexer(code)
    parser = Parser(lexer)
    program = parser.parse_program()
    if parser.errors:
        raise RuntimeError(f"Parse Error: {parser.errors}")
    env = Environment()
    result = evaluator.eval(program, env)
    return result, env, output_list

class TestDualKeywords(unittest.TestCase):
    def test_english_variable_and_print(self):
        code = '''
        let x = 42;
        print(x);
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(out, ["42"])
        self.assertEqual(env.get("x").value, 42)

    def test_english_function_declaration_and_call(self):
        code = '''
        fn add(a, b)
            return a + b;
        end
        let sum = add(15, 25);
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("sum").value, 40)

    def test_english_if_else(self):
        code = '''
        let status = "";
        if true
            status = "yes";
        else
            status = "no";
        end
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("status").value, "yes")

    def test_english_while_loop(self):
        code = '''
        let count = 0;
        let sum = 0;
        while count < 5
            sum += count;
            count += 1;
        end
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("sum").value, 10)

    def test_english_for_in_loop(self):
        code = '''
        let total = 0;
        for num in [10, 20, 30]
            total += num;
        end
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("total").value, 60)

    def test_english_try_catch_throw(self):
        code = '''
        let caught = "";
        try
            throw "custom error";
        catch err
            caught = err;
        end
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("caught").value, "custom error")

    def test_boolean_and_null_keywords(self):
        code = '''
        let a = true;
        let b = false;
        let c = null;
        let d = nil;
        let e = not false;
        let f = true and false;
        let g = false or true;
        '''
        res, env, out = run_dhi(code)
        self.assertTrue(env.get("a").value)
        self.assertFalse(env.get("b").value)
        self.assertIsInstance(env.get("c"), DhicodeNull)
        self.assertIsInstance(env.get("d"), DhicodeNull)
        self.assertTrue(env.get("e").value)
        self.assertFalse(env.get("f").value)
        self.assertTrue(env.get("g").value)


class TestConstantsAndImmutability(unittest.TestCase):
    def test_const_declaration_and_access(self):
        code = '''
        const PI = 3.14159;
        const GREETING = "Hello";
        '''
        res, env, out = run_dhi(code)
        self.assertAlmostEqual(env.get("PI").value, 3.14159)
        self.assertEqual(env.get("GREETING").value, "Hello")

    def test_dhivehi_const_declaration(self):
        code = '''
        ދާއިމީ އަގެއް = 100;
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("އަގެއް").value, 100)

    def test_const_reassignment_error(self):
        code = '''
        const X = 10;
        X = 20;
        '''
        res, env, out = run_dhi(code)
        self.assertIsInstance(res, DhicodeError)
        self.assertIn("ދާއިމީ", res.message)

    def test_const_compound_assignment_error(self):
        code = '''
        const COUNT = 5;
        COUNT += 1;
        '''
        res, env, out = run_dhi(code)
        self.assertIsInstance(res, DhicodeError)
        self.assertIn("ދާއިމީ", res.message)

    def test_const_redeclaration_error(self):
        code = '''
        const MAX = 100;
        let MAX = 200;
        '''
        res, env, out = run_dhi(code)
        self.assertIsInstance(res, DhicodeError)
        self.assertIn("ދާއިމީ", res.message)


class TestAssignmentAndCompoundOperators(unittest.TestCase):
    def test_variable_reassignment(self):
        code = '''
        let a = 1;
        a = 2;
        a = a + 3;
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("a").value, 5)

    def test_compound_assignments(self):
        code = '''
        let x = 10;
        x += 5;
        x -= 3;
        x *= 2;
        x /= 4;
        x %= 4;
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("x").value, 2)

    def test_list_index_assignment(self):
        code = '''
        let items = [10, 20, 30];
        items[1] = 99;
        items[0] += 5;
        '''
        res, env, out = run_dhi(code)
        lst = env.get("items")
        self.assertEqual([x.value for x in lst.elements], [15, 99, 30])

    def test_dict_index_assignment(self):
        code = '''
        let data = {"name": "Ali"};
        data["age"] = 25;
        data["name"] = "Ahmed";
        '''
        res, env, out = run_dhi(code)
        d = env.get("data")
        self.assertEqual(d.pairs["name"].value, "Ahmed")
        self.assertEqual(d.pairs["age"].value, 25)


class TestExponentiation(unittest.TestCase):
    def test_basic_power(self):
        code = '''
        let a = 2 ** 3;
        let b = 10 ** 0;
        let c = 5 ** 2;
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("a").value, 8)
        self.assertEqual(env.get("b").value, 1)
        self.assertEqual(env.get("c").value, 25)

    def test_power_right_associativity(self):
        code = '''
        let x = 2 ** 3 ** 2; // 2 ** (3 ** 2) = 2 ** 9 = 512
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("x").value, 512)


class TestNullCoalescing(unittest.TestCase):
    def test_null_coalescing_with_null(self):
        code = '''
        let a = null ?? "default";
        let b = nil ?? 100;
        let c = ހުސް ?? "ދިވެހި";
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("a").value, "default")
        self.assertEqual(env.get("b").value, 100)
        self.assertEqual(env.get("c").value, "ދިވެހި")

    def test_null_coalescing_with_non_null(self):
        code = '''
        let a = "hello" ?? "default";
        let b = 0 ?? 42;
        let c = false ?? true;
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("a").value, "hello")
        self.assertEqual(env.get("b").value, 0)
        self.assertFalse(env.get("c").value)

    def test_null_coalescing_short_circuit(self):
        code = '''
        let evaluated = false;
        fn side_effect()
            evaluated = true;
            return 999;
        end
        let res = "keep" ?? side_effect();
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("res").value, "keep")
        self.assertFalse(env.get("evaluated").value)


class TestBitwiseOperators(unittest.TestCase):
    def test_bitwise_operations(self):
        code = '''
        let band = 5 & 3;   // 101 & 011 = 001 (1)
        let bor  = 5 | 2;   // 101 | 010 = 111 (7)
        let bxor = 5 ^ 1;   // 101 ^ 001 = 100 (4)
        let bnot = ~0;      // -1
        let bshl = 1 << 3;  // 8
        let bshr = 16 >> 2; // 4
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("band").value, 1)
        self.assertEqual(env.get("bor").value, 7)
        self.assertEqual(env.get("bxor").value, 4)
        self.assertEqual(env.get("bnot").value, -1)
        self.assertEqual(env.get("bshl").value, 8)
        self.assertEqual(env.get("bshr").value, 4)


class TestStringInterpolation(unittest.TestCase):
    def test_basic_interpolation(self):
        code = '''
        let name = "އަޙްމަދު";
        let greeting = "މަރުޙަބާ {name}!";
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("greeting").value, "މަރުޙަބާ އަޙްމަދު!")

    def test_expression_interpolation(self):
        code = '''
        let calc = "2 + 3 = {2 + 3}";
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("calc").value, "2 + 3 = 5")

    def test_escaped_braces(self):
        code = '''
        let raw = "literal \\{braces\\}";
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("raw").value, "literal {braces}")


class TestEnglishBuiltins(unittest.TestCase):
    def test_builtins_english_names(self):
        code = '''
        let l = len([1, 2, 3, 4]);
        let t = type("text");
        let d = {"a": 10};
        let k = keys(d);
        let v = values(d);
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("l").value, 4)
        self.assertEqual(env.get("t").value, "ލިޔުން")
        self.assertEqual(len(env.get("k").elements), 1)
        self.assertEqual(len(env.get("v").elements), 1)

if __name__ == "__main__":
    unittest.main()
