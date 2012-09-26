#coding: utf-8

import unittest
import kml.parser as parser
import kml.scheme as scheme
import time
from flask import *

app = Flask(__name__);

class TestCase(unittest.TestCase):
    def setUp(self):
        pass;
    def tearDown(self):
        pass;
    def test_test(self):
        self.assertEqual(1, 1);

@app.route("/", methods=["GET", "POST"])
def main():
    text = "";
    if (request.method == "GET"):
        pass;
    else:
        sc = scheme.SchemeReader(text=request.form["siml"].encode("utf-8"));
        out = parser.Parser(sc, request.form["url"]);
        text = out.text;

    print text
    return render_template("main.html", text=text);
    #return text

if __name__ == "__main__":
    app.debug = True;
    app.run();
