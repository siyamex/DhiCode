# tests/test_phase3_oop_and_modern_syntax.py
import unittest
from lexer import Lexer
from parser import Parser
from evaluator import Evaluator, Environment, DhicodeNumber, DhicodeString, DhicodeBoolean, DhicodeNull, DhicodeList, DhicodeDict, DhicodeInstance, DhicodeClass

class TestPhase3OOPAndModernSyntax(unittest.TestCase):
    def eval_code(self, source):
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program()
        self.assertEqual(parser.errors, [], f"Parser errors: {parser.errors}")

        output = []
        evaluator = Evaluator(output_callback=lambda s: output.append(s))
        env = Environment()
        result = evaluator.eval(program, env)
        return result, env, output

    # 1. Classes, Objects & Methods
    def test_class_creation_and_method_call(self):
        code = """
        class Person {
            fn constructor(name, age) {
                this.name = name;
                this.age = age;
            }

            fn getInfo() {
                return this.name + " (" + this.age + ")";
            }

            fn haveBirthday() {
                this.age += 1;
                return this.age;
            }
        }

        let p = Person("Aminath", 25);
        let info = p.getInfo();
        let new_age = p.haveBirthday();
        """
        _, env, _ = self.eval_code(code)
        p = env.get("p")
        self.assertIsInstance(p, DhicodeInstance)
        self.assertEqual(env.get("info").value, "Aminath (25)")
        self.assertEqual(env.get("new_age").value, 26)
        self.assertEqual(p.fields["age"].value, 26)

    def test_dhivehi_class_and_inheritance(self):
        code = """
        ކްލާސް އިންސާނާ
            ވަޒީފާ ހަދާ_ވަޒީފާ(ނަން, އުމުރު)
                މި.ނަން = ނަން
                މި.އުމުރު = އުމުރު
            ނިމުނީ

            ވަޒީފާ ނަން_ހޯދާ()
                ފޮނުވާ މި.ނަން
            ނިމުނީ
        ނިމުނީ

        ކްލާސް ދަރިވަރު ދަރިކޮޅު އިންސާނާ
            ވަޒީފާ ހަދާ_ވަޒީފާ(ނަން, އުމުރު, ސްކޫލް)
                މި.ނަން = ނަން
                މި.އުމުރު = އުމުރު
                މި.ސްކޫލް = ސްކޫލް
            ނިމުނީ

            ވަޒީފާ ތަޢާރަފް()
                ފޮނުވާ މި.ނަން_ހޯދާ() + " - " + މި.ސްކޫލް
            ނިމުނީ
        ނިމުނީ

        ކަނޑައަޅާ ދ = ދަރިވަރު("ޢަލީ", 16, "މަޖީދިއްޔާ");
        ކަނޑައަޅާ ނަތީޖާ = ދ.ތަޢާރަފް();
        """
        _, env, _ = self.eval_code(code)
        self.assertEqual(env.get("ނަތީޖާ").value, "ޢަލީ - މަޖީދިއްޔާ")

    # 2. Dot Property Access & Mutation
    def test_dot_access_and_mutation_dict(self):
        code = """
        let user = { name: "Ibrahim", score: 50 };
        let initial_score = user.score;
        user.score += 25;
        let final_score = user.score;
        """
        _, env, _ = self.eval_code(code)
        self.assertEqual(env.get("initial_score").value, 50)
        self.assertEqual(env.get("final_score").value, 75)

    # 3. Default Parameter Values
    def test_default_parameters(self):
        code = """
        fn greet(name, greeting = "Hello") {
            return greeting + " " + name;
        }

        let g1 = greet("Mariyam");
        let g2 = greet("Mariyam", "Good morning");
        """
        _, env, _ = self.eval_code(code)
        self.assertEqual(env.get("g1").value, "Hello Mariyam")
        self.assertEqual(env.get("g2").value, "Good morning Mariyam")

    # 4. Variadic Arguments (...args)
    def test_variadic_parameters(self):
        code = """
        fn calculate_sum(...numbers) {
            let total = 0;
            for n in numbers {
                total += n;
            }
            return total;
        }

        let s1 = calculate_sum();
        let s2 = calculate_sum(1, 2, 3, 4, 5);
        """
        _, env, _ = self.eval_code(code)
        self.assertEqual(env.get("s1").value, 0)
        self.assertEqual(env.get("s2").value, 15)

    # 5. Arrow Functions & Lambdas
    def test_arrow_functions(self):
        code = """
        let square = (x) => x * x;
        let add = (a, b = 5) => a + b;
        let multiline = (x) => {
            let y = x * 2;
            return y + 1;
        };

        let res1 = square(6);
        let res2 = add(10);
        let res3 = add(10, 20);
        let res4 = multiline(5);
        """
        _, env, _ = self.eval_code(code)
        self.assertEqual(env.get("res1").value, 36)
        self.assertEqual(env.get("res2").value, 15)
        self.assertEqual(env.get("res3").value, 30)
        self.assertEqual(env.get("res4").value, 11)

    def test_anonymous_function_expressions(self):
        code = """
        let f = fn(x) => x * 10;
        let res = f(7);
        """
        _, env, _ = self.eval_code(code)
        self.assertEqual(env.get("res").value, 70)

    # 6. Range Operator (..)
    def test_range_operator(self):
        code = """
        let ascending = 1..5;
        let descending = 5..1;

        let total = 0;
        for x in 1..4 {
            total += x;
        }
        """
        _, env, _ = self.eval_code(code)
        asc = env.get("ascending")
        self.assertIsInstance(asc, DhicodeList)
        self.assertEqual([n.value for n in asc.elements], [1, 2, 3, 4, 5])

        desc = env.get("descending")
        self.assertIsInstance(desc, DhicodeList)
        self.assertEqual([n.value for n in desc.elements], [5, 4, 3, 2, 1])

        self.assertEqual(env.get("total").value, 10)

    # 7. Destructuring Assignment
    def test_list_destructuring(self):
        code = """
        let [a, b, c] = [10, 20, 30];
        const [x, y] = [100, 200];
        """
        _, env, _ = self.eval_code(code)
        self.assertEqual(env.get("a").value, 10)
        self.assertEqual(env.get("b").value, 20)
        self.assertEqual(env.get("c").value, 30)
        self.assertEqual(env.get("x").value, 100)
        self.assertEqual(env.get("y").value, 200)

    def test_dict_destructuring(self):
        code = """
        let person = { name: "Ahmed", age: 30 };
        let {name, age} = person;
        """
        _, env, _ = self.eval_code(code)
        self.assertEqual(env.get("name").value, "Ahmed")
        self.assertEqual(env.get("age").value, 30)

    def test_dhivehi_destructuring(self):
        code = """
        ކަނޑައަޅާ [ރ1, ރ2] = ["މާލެ", "ވިލިމާލެ"];
        ކަނޑައަޅާ {އަގު1, އަގު2} = { އަގު1: 100, އަގު2: 200 };
        """
        _, env, _ = self.eval_code(code)
        self.assertEqual(env.get("ރ1").value, "މާލެ")
        self.assertEqual(env.get("ރ2").value, "ވިލިމާލެ")
        self.assertEqual(env.get("އަގު1").value, 100)
        self.assertEqual(env.get("އަގު2").value, 200)

    # 8. Print with multiple arguments
    def test_print_multiple_arguments(self):
        code = """
        print("A", 1, true);
        print("Single");
        """
        _, _, output = self.eval_code(code)
        self.assertEqual(output, ["A 1 އާން", "Single"])

if __name__ == "__main__":
    unittest.main()
