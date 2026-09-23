# tests/test_phase4_backend_and_database.py
# Comprehensive tests for Phase 4: SQLite Database & Native HTTP Web Server

import unittest
import os
import time
import shutil
import urllib.request
import json

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

class TestPhase4Database(unittest.TestCase):
    def test_sqlite_in_memory_basic_english(self):
        code = '''
        import "db";
        let db_conn = open(":memory:");
        db_conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);");
        db_conn.execute("INSERT INTO users (name, age) VALUES (?, ?);", ["Ahmed", 28]);
        db_conn.execute("INSERT INTO users (name, age) VALUES (?, ?);", ["Mariyam", 24]);

        let users = db_conn.query("SELECT * FROM users ORDER BY id;");
        let first = users[0];
        let second = users[1];
        let tables = db_conn.tables();
        db_conn.close();
        '''
        res, env, out = run_dhi(code)
        users = env.get("users")
        self.assertIsInstance(users, DhicodeList)
        self.assertEqual(len(users.elements), 2)

        first = env.get("first")
        self.assertEqual(first.pairs["name"].value, "Ahmed")
        self.assertEqual(first.pairs["age"].value, 28)

        second = env.get("second")
        self.assertEqual(second.pairs["name"].value, "Mariyam")
        self.assertEqual(second.pairs["age"].value, 24)

        tables = env.get("tables")
        self.assertIn("users", [t.value for t in tables.elements])

    def test_sqlite_dhivehi_syntax(self):
        code = '''
        ގެނޭ "ޑޭޓާބޭސް";
        ކަނޑައަޅާ ޑީބީ = ހުޅުވާ(":memory:");
        ޑީބީ.ހިންގާ("CREATE TABLE atolls (code TEXT PRIMARY KEY, name TEXT);");
        ޑީބީ.ހިންގާ("INSERT INTO atolls (code, name) VALUES (?, ?);", ["K", "ކާފު"]);
        ޑީބީ.ހިންގާ("INSERT INTO atolls (code, name) VALUES (?, ?);", ["AA", "އަރިއަތޮޅު އުތުރުބުރި"]);

        ކަނޑައަޅާ ނަތީޖާ = ޑީބީ.ހޯދާ("SELECT * FROM atolls WHERE code = ?;", ["K"]);
        ކަނޑައަޅާ އެކަތި = ޑީބީ.އެކަތި_ހޯދާ("SELECT * FROM atolls WHERE code = ?;", ["AA"]);
        ޑީބީ.ލައްޕާ();
        '''
        res, env, out = run_dhi(code)
        results = env.get("ނަތީޖާ")
        self.assertEqual(len(results.elements), 1)
        self.assertEqual(results.elements[0].pairs["name"].value, "ކާފު")

        single = env.get("އެކަތި")
        self.assertEqual(single.pairs["name"].value, "އަރިއަތޮޅު އުތުރުބުރި")

    def test_sqlite_transaction_and_rollback(self):
        code = '''
        import "db";
        let conn = open(":memory:");
        conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance INTEGER);");
        conn.execute("INSERT INTO accounts (balance) VALUES (?);", [1000]);

        conn.begin();
        conn.execute("UPDATE accounts SET balance = balance - 200 WHERE id = 1;");
        conn.rollback();

        let row1 = conn.query_one("SELECT balance FROM accounts WHERE id = 1;");

        conn.begin();
        conn.execute("UPDATE accounts SET balance = balance + 500 WHERE id = 1;");
        conn.commit();

        let row2 = conn.query_one("SELECT balance FROM accounts WHERE id = 1;");
        conn.close();
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("row1").pairs["balance"].value, 1000)
        self.assertEqual(env.get("row2").pairs["balance"].value, 1500)

    def test_sqlite_execute_many(self):
        code = '''
        import "db";
        let conn = open(":memory:");
        conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, title TEXT);");
        let batch = [["Huni Roshi"], ["Kulhi Boakibaa"], ["Foni Boakibaa"]];
        conn.execute_many("INSERT INTO items (title) VALUES (?);", batch);

        let count_row = conn.query_one("SELECT count(*) as total FROM items;");
        let total = count_row["total"];
        conn.close();
        '''
        res, env, out = run_dhi(code)
        self.assertEqual(env.get("total").value, 3)

    def test_sqlite_file_backed_database(self):
        db_file = "test_phase4_temp.db"
        if os.path.exists(db_file):
            os.remove(db_file)

        try:
            code = f'''
            import "db";
            let db1 = open("{db_file}");
            db1.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY, note TEXT);");
            db1.execute("INSERT INTO notes (note) VALUES (?);", ["DhiCode Phase 4"]);
            db1.close();

            let db2 = open("{db_file}");
            let rows = db2.query("SELECT note FROM notes;");
            let msg = rows[0]["note"];
            db2.close();
            '''
            res, env, out = run_dhi(code)
            self.assertEqual(env.get("msg").value, "DhiCode Phase 4")
        finally:
            if os.path.exists(db_file):
                os.remove(db_file)


class TestPhase4HTTPServer(unittest.TestCase):
    def test_http_serve_basic(self):
        code = '''
        import "net";
        fn handler(req) {
            return {
                "status": 200,
                "body": "Hello from DHicode Web Server!",
                "headers": {"X-Custom-Header": "DHICODE-4"}
            };
        }

        let server = serve(0, handler, {"background": true});
        let url = "http://127.0.0.1:" + server.port + "/test";
        let client_res = get(url);
        server.close();
        '''
        res, env, out = run_dhi(code)
        client_res = env.get("client_res")
        self.assertEqual(client_res.pairs["status"].value, 200)
        self.assertEqual(client_res.pairs["body"].value, "Hello from DHicode Web Server!")
        headers = client_res.pairs["headers"]
        self.assertIn("x-custom-header", [k.lower() for k in headers.pairs.keys()])

    def test_http_router_and_json_response(self):
        code = '''
        import "net";
        let router = create_router();

        router.get("/hello", fn(req) {
            return response_json({"message": "Hello World", "query": req.query});
        });

        router.post("/echo", fn(req) {
            return response_json({"received": req.json}, 201);
        });

        let server = serve(0, router, {"background": true});
        let base_url = "http://127.0.0.1:" + server.port;

        let get_res = get(base_url + "/hello?name=Ali&island=Male");
        let post_res = post(base_url + "/echo", {"title": "Test Title", "votes": 42});
        let not_found_res = get(base_url + "/nonexistent");

        server.close();
        '''
        res, env, out = run_dhi(code)
        get_res = env.get("get_res")
        self.assertEqual(get_res.pairs["status"].value, 200)
        json_data = get_res.pairs["json"]
        self.assertEqual(json_data.pairs["message"].value, "Hello World")
        query_data = json_data.pairs["query"]
        self.assertEqual(query_data.pairs["name"].value, "Ali")
        self.assertEqual(query_data.pairs["island"].value, "Male")

        post_res = env.get("post_res")
        self.assertEqual(post_res.pairs["status"].value, 201)
        post_json = post_res.pairs["json"]
        received = post_json.pairs["received"]
        self.assertEqual(received.pairs["title"].value, "Test Title")
        self.assertEqual(received.pairs["votes"].value, 42)

        not_found_res = env.get("not_found_res")
        self.assertEqual(not_found_res.pairs["status"].value, 404)

    def test_http_dhivehi_web_service_with_database(self):
        code = '''
        ގެނޭ "ނެޓްވޯކް";
        ގެނޭ "ޑޭޓާބޭސް";

        ކަނޑައަޅާ ޑީބީ = ހުޅުވާ(":memory:");
        ޑީބީ.ހިންގާ("CREATE TABLE islands (id INTEGER PRIMARY KEY, name TEXT, atoll TEXT);");
        ޑީބީ.ހިންގާ("INSERT INTO islands (name, atoll) VALUES (?, ?);", ["މާލެ", "ކ"]);
        ޑީބީ.ހިންގާ("INSERT INTO islands (name, atoll) VALUES (?, ?);", ["ހުޅުމާލެ", "ކ"]);
        ޑީބީ.ހިންގާ("INSERT INTO islands (name, atoll) VALUES (?, ?);", ["ކުޅުދުއްފުށި", "ހދ"]);

        ކަނޑައަޅާ ރ = ރައުޓަރ_ހަދާ();

        ރ.ނަގާ("/islands", ވަޒީފާ(އެދުން) {
            ކަނޑައަޅާ ބަރިތައް = ޑީބީ.ހޯދާ("SELECT * FROM islands;");
            އަނބުރާ ޖޭސަން_ޖަވާބު(ބަރިތައް);
        });

        ކަނޑައަޅާ ސ = ސާވަރު(0, ރ, {"background": އާން});
        ކަނޑައަޅާ ލިބުނު = ނަގާ("http://127.0.0.1:" + ސ.port + "/islands");
        ސ.ލައްޕާ();
        ޑީބީ.ލައްޕާ();
        '''
        res, env, out = run_dhi(code)
        res_obj = env.get("ލިބުނު")
        self.assertEqual(res_obj.pairs["status"].value, 200)
        items = res_obj.pairs["json"]
        self.assertEqual(len(items.elements), 3)
        self.assertEqual(items.elements[0].pairs["name"].value, "މާލެ")
        self.assertEqual(items.elements[1].pairs["name"].value, "ހުޅުމާލެ")
        self.assertEqual(items.elements[2].pairs["name"].value, "ކުޅުދުއްފުށި")

if __name__ == "__main__":
    unittest.main()
