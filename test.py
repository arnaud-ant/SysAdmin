# pylint: disable=missing-function-docstring,missing-module-docstring,wildcard-import,no-member,unused-wildcard-import,missing-class-docstring
import unittest

from Script import *

class TestMethods(unittest.TestCase):


    def test_datatransform(self):
        dataInit = ['              total        used        free      shared  buff/cache\
   available\nMem:        2045616       88504     1617704       21192      339408\
     1787740\nSwap:             0           0           0\n', 'cpu  12384 17 8956\
 58135814 12461 0 62 22 0 0\ncpu0 12384 17 8956 58135814 12461 0 62 22 0 0\nintr 6318068\
 8 9 0 0 2165 0 0 0 0 0 58173 988 3 0 0 0 0 0 0 0 0 0 0 0 0 183047 0 117262 4 0 0 0 0 0 0\
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\nctxt\
 12163896\nbtime 1638808288\nprocesses 31720\nprocs_running 1\nprocs_blocked 0\nsoftirq\
 3003383 0 2085146 11551 117455 0 0 1 0 21 789209\n', 52.06704139709473]
        expectedData = [4.32652071552041, 0.015612593422298485, 52]
        self.assertEqual(expectedData, TransformData(dataInit))

    def test_getlog(self):
        dataInit = '127.0.0.1 - - [07/Dec/2021:12:26:56 +0100] "GET /favicon.ico\
 HTTP/1.1" 404 487 "http://localhost/page1.html" "Mozilla/5.0 (X11; Ubuntu;\
 Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"\n127.0.0.1 - -\
 [07/Dec/2021:12:27:01 +0100] "GET /index.html HTTP/1.1" 200 3477 "-"\
 "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"\
\n127.0.0.1 - - [07/Dec/2021:12:27:02 +0100] "GET /favicon.ico HTTP/1.1" 404 487\
 "http://localhost/index.html" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0)\
 Gecko/20100101 Firefox/94.0"\n127.0.0.1 - - [07/Dec/2021:12:27:14 +0100] "GET\
 /index.html HTTP/1.1" 200 3477 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0)\
 Gecko/20100101 Firefox/94.0"\n127.0.0.1 - - [07/Dec/2021:12:27:15 +0100] "GET /favicon.ico\
 HTTP/1.1" 404 487 "http://localhost/index.html" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0)\
 Gecko/20100101 Firefox/94.0"'
        expectedData = [["127.0.0.1", "07/Dec/2021:12:26:56", "/favicon.ico", "404"],
                        ["127.0.0.1", "07/Dec/2021:12:27:01", "/index.html", "200"],
                        ["127.0.0.1", "07/Dec/2021:12:27:02", "/favicon.ico", "404"],
                        ["127.0.0.1", "07/Dec/2021:12:27:14", "/index.html", "200"],
                        ["127.0.0.1", "07/Dec/2021:12:27:15", "/favicon.ico", "404"]]
        self.assertEqual(expectedData, GetLog(dataInit))

    def testnb404(self):
        dataInit = [["127.0.0.1", "07/Dec/2021:12:26:56", "/favicon.ico", "404"],
                    ["127.0.0.1", "07/Dec/2021:12:27:01", "/index.html", "200"],
                    ["127.0.0.1", "07/Dec/2021:12:27:02", "/favicon.ico", "404"],
                    ["127.0.0.1", "07/Dec/2021:12:27:14", "/index.html", "200"],
                    ["127.0.0.1", "07/Dec/2021:12:27:15", "/favicon.ico", "404"]]
        expectedData = 3
        self.assertEqual(expectedData, GetNb404(dataInit))

    def test_getactivitylastminute(self):
        dataInit = "278 /var/log/appache2/access.log"
        expectedData = 278
        self.assertEqual(expectedData, GetActivityLastMinute(dataInit))

    def test_getstatbypage(self):
        dataInit = [["127.0.0.1", "07/Dec/2021:12:26:56", "/favicon.ico", "404"],
                    ["127.0.0.1", "07/Dec/2021:12:27:01", "/index.html", "200"],
                    ["127.0.0.1", "07/Dec/2021:12:27:02", "/favicon.ico", "404"],
                    ["127.0.0.1", "07/Dec/2021:12:27:14", "/index.html", "200"],
                    ["127.0.0.1", "07/Dec/2021:12:27:15", "/favicon.ico", "404"]]
        expectedData = {"/favicon.ico":3, "/index.html":2}
        self.assertEqual(expectedData, GetStatByPage(dataInit))

    def test_fusiondico(self):
        dicoA = {"a":1, "b":2}
        dicoB = {"a":2, "c":3}
        expectedData = {"a":3, "b":2, "c":3}
        self.assertEqual(expectedData, FusionDico(dicoA, dicoB))

    def test_getstatbyconnection(self):
        dataInit = [["127.0.0.1", "07/Dec/2021:12:26:56", "/favicon.ico", "404"],
                    ["127.0.0.1", "07/Dec/2021:12:27:01", "/index.html", "200"],
                    ["127.0.0.1", "07/Dec/2021:12:27:02", "/favicon.ico", "404"],
                    ["127.0.0.1", "07/Dec/2021:12:27:14", "/index.html", "200"],
                    ["127.0.0.1", "07/Dec/2021:12:27:15", "/favicon.ico", "404"]]
        expectedData = {"127.0.0.1":5}
        self.assertEqual(expectedData, GetStatByConnection(dataInit))

    def test_regex(self):
        self.assertRegex(
            "127.0.0.1", "^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$")  # Test Ip
        self.assertRegex("09/Jan/2020:10:35:48",
                         "^(3[0-1]|[0-2][0-9])/[A-Z][a-z]+/[0-9]{4}"+
                         ":([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$")
        # Test date
        self.assertRegex("404", "[1-5][0-9]{2}")  # Test Return Code http
        self.assertRegex("/index.html", "^/.*?")  # Test Page


if __name__ == '__main__':
    TestMethods().runtest()
