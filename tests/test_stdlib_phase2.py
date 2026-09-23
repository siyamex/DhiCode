# tests/test_stdlib_phase2.py
import unittest
import os
import shutil
from lexer import Lexer
from parser import Parser
from evaluator import Evaluator, Environment, DhicodeNumber, DhicodeString, DhicodeBoolean, DhicodeNull, DhicodeDict, DhicodeList

def run_dhi(code: str):
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

class TestDualModuleImports(unittest.TestCase):
    def test_english_math_import(self):
        code = '''
        import "math";
        let a = sqrt(64);
        let b = round(3.7);
        let c = abs(-10);
        let p = pi;
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("a").value, 8)
        self.assertEqual(env.get("b").value, 4)
        self.assertEqual(env.get("c").value, 10)
        self.assertAlmostEqual(env.get("p").value, 3.141592653589793)

    def test_dhivehi_math_import(self):
        code = '''
        ގެނޭ "ހިސާބު";
        ކަނޑައަޅާ އަ = ޖަޒުރު(64);
        ކަނޑައަޅާ ބ = މުތުލަޤު(-15);
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("އަ").value, 8)
        self.assertEqual(env.get("ބ").value, 15)

    def test_english_crypto_import(self):
        code = '''
        import "crypto";
        let h = sha256("test");
        let b = base64_encode("hello world");
        let d = base64_decode(b);
        '''
        res, env, out = run_dhi(code)
        import hashlib, base64
        expected_h = hashlib.sha256(b"test").hexdigest()
        self.assertEqual(env.get("h").value, expected_h)
        self.assertEqual(env.get("d").value, "hello world")

    def test_english_regex_import(self):
        code = '''
        import "regex";
        let is_num = match("^\\d+$", "12345");
        let is_not_num = match("^\\d+$", "123a5");
        let rep = replace("\\s+", "_", "a b c");
        '''
        res, env, out = run_dhi(code)
        self.assertTrue(env.get("is_num").value)
        self.assertFalse(env.get("is_not_num").value)
        self.assertEqual(env.get("rep").value, "a_b_c")


class TestMathExtensions(unittest.TestCase):
    def test_trigonometry_and_log(self):
        code = '''
        import "math";
        let s = sin(0);
        let c = cos(0);
        let l = log(100, 10);
        let euler = e;
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("s").value, 0)
        self.assertEqual(env.get("c").value, 1)
        self.assertAlmostEqual(env.get("l").value, 2.0)
        self.assertAlmostEqual(env.get("euler").value, 2.718281828459045)


class TestFileSystemExtensions(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_sandbox_phase2"
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_file_and_directory_ops(self):
        code = f'''
        import "file";
        let ok_dir = mkdir("{self.test_dir}");
        let dir_exists = exists("{self.test_dir}");
        let test_file = "{self.test_dir}/hello.txt";
        let ok_write = write(test_file, "DhiCode 2026");
        let file_exists = exists(test_file);
        let s = file_size(test_file);
        let files = list_dir("{self.test_dir}");
        let ok_del = delete(test_file);
        let file_deleted = exists(test_file);
        let ok_del_dir = delete("{self.test_dir}");
        '''
        res, env, out = run_dhi(code)
        self.assertTrue(env.get("ok_dir").value)
        self.assertTrue(env.get("dir_exists").value)
        self.assertTrue(env.get("file_exists").value)
        self.assertEqual(env.get("s").value, 12)
        self.assertEqual([e.value for e in env.get("files").elements], ["hello.txt"])
        self.assertFalse(env.get("file_deleted").value)


class TestTimeAndSystemExtensions(unittest.TestCase):
    def test_time_and_system(self):
        code = '''
        import "time";
        import "os";
        let ts = timestamp(2026, 9, 23, 12, 0, 0);
        let plat = platform();
        let path = cwd();
        '''
        res, env, out = run_dhi(code)
        self.assertGreater(env.get("ts").value, 0)
        self.assertIsInstance(env.get("plat").value, str)
        self.assertIsInstance(env.get("path").value, str)


class TestNakaiyExtensions(unittest.TestCase):
    def test_monsoon_and_nakaiy_day(self):
        code = '''
        import "nakaiy";
        let m_hulhangu = monsoon(5, 10);
        let m_iruvai = monsoon(1, 10);
        let kethi_day = nakaiy_day(5, 8); // Kethi starts 05-06, day 3
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("m_hulhangu").value, "ހުޅަނގު")
        self.assertEqual(env.get("m_iruvai").value, "އިރުވައި")
        self.assertEqual(env.get("kethi_day").value, 3)


class TestPrayerAndHijri(unittest.TestCase):
    def test_prayer_times_and_hijri(self):
        code = '''
        import "prayer";
        let atoll_list = atolls();
        let hijri = hijri_date(2026, 9, 23);
        '''
        res, env, out = run_dhi(code)
        atolls = [x.value for x in env.get("atoll_list").elements]
        self.assertIn("މާލެ", atolls)
        self.assertIn("އައްޑޫ", atolls)

        hijri_dict = env.get("hijri")
        self.assertEqual(hijri_dict.pairs["year"].value, 1448)
        self.assertEqual(hijri_dict.pairs["month_num"].value, 4)


class TestThaanaTools(unittest.TestCase):
    def test_thaana_utilities(self):
        code = '''
        import "thaana";
        let is_t = is_thaana("މާލެ");
        let is_not_t = is_thaana("Male City");
        let stripped = strip_fili("ދިވެހި");
        let mvr_val = currency_mvr(1500.5);
        let latin_word = to_latin("ދިވެހި");
        let latin_city = to_latin("މާލެ");
        let latin_nation = to_latin("ރާއްޖެ");
        '''
        res, env, out = run_dhi(code)
        self.assertTrue(env.get("is_t").value)
        self.assertFalse(env.get("is_not_t").value)
        self.assertEqual(env.get("stripped").value, "ދވހ")
        self.assertEqual(env.get("mvr_val").value, "ރ. 1,500.50")
        self.assertEqual(env.get("latin_word").value, "dhivehi")
        self.assertEqual(env.get("latin_city").value, "maale")
        self.assertEqual(env.get("latin_nation").value, "raajje")


class TestCryptoAndRegex(unittest.TestCase):
    def test_crypto_algorithms(self):
        code = '''
        import "crypto";
        let s256 = sha256("dhicode");
        let s512 = sha512("dhicode");
        let m5 = md5("dhicode");
        let mac = hmac_sha256("key", "data");
        let tok = random_token(16);
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(len(env.get("s256").value), 64)
        self.assertEqual(len(env.get("s512").value), 128)
        self.assertEqual(len(env.get("m5").value), 32)
        self.assertEqual(len(env.get("mac").value), 64)
        self.assertEqual(len(env.get("tok").value), 32)

    def test_regex_operations(self):
        code = '''
        import "regex";
        let search_res = search("(\\d+)", "item: 789 units");
        let split_res = split(",", "apple,orange,banana");
        let rep_res = replace("fox", "cat", "the quick brown fox");
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("search_res").pairs["text"].value, "789")
        self.assertEqual([x.value for x in env.get("split_res").elements], ["apple", "orange", "banana"])
        self.assertEqual(env.get("rep_res").value, "the quick brown cat")

if __name__ == "__main__":
    unittest.main()
