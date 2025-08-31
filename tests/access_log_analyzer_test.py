import unittest
from scripts.access_log_analyzer import input_file, extract_data_from_file
from unittest.mock import patch

class UnitTests(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "/Users/danielhall/Desktop/Automation/Python Scripts/tests/access_log_analyzer_test.py"])   # simulate input
    def test_input_file(self, mock_input):
        result = input_file()
        self.assertEqual(result, ("1", "/Users/danielhall/Desktop/Automation/Python Scripts/tests/access_log_analyzer_test.py"))

    def test_extracted_data_from_apache_combined_format_file(self):
        result = extract_data_from_file("1", "/Users/danielhall/Desktop/Automation/Python Scripts/tests/access_log_analyzer_test.py")
        extracted_dict_list = [
            {
                "ip": "161.90.170.15",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "PUT",
                "path": "/static/js/app.js",
                "protocol": "HTTP/1.1",
                "status": 503,
                "size": 3733,
                "referer": "http://example.com/index.html",
                "user_agent": "Wget/1.20.3 (linux-gnu)"
            },
            {
                "ip": "203.97.89.211",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "PUT",
                "path": "/products",
                "protocol": "HTTP/1.1",
                "status": 404,
                "size": 4299,
                "referer": "http://example.com/api/data",
                "user_agent": "curl/7.68.0"
            },
            {
                "ip": "201.27.135.197",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "DELETE",
                "path": "/products",
                "protocol": "HTTP/1.1",
                "status": 502,
                "size": 1989,
                "referer": "http://example.com/products",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15"
            },
            {
                "ip": "209.170.108.103",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "DELETE",
                "path": "/favicon.ico",
                "protocol": "HTTP/1.1",
                "status": 403,
                "size": 1449,
                "referer": "http://example.com/login",
                "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Firefox/113.0"
            },
            {
                "ip": "169.194.217.47",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "DELETE",
                "path": "/dashboard",
                "protocol": "HTTP/1.1",
                "status": 401,
                "size": 2312,
                "referer": "http://example.com/api/data",
                "user_agent": "Wget/1.20.3 (linux-gnu)"
            }
        ]
        self.assertEqual(result, extracted_dict_list)
    
    def test_extracted_data_from_apache_common_format_file(self):
        result = extract_data_from_file("2", "/Users/danielhall/Desktop/Automation/Python Scripts/tests/access_log_analyzer_test.py")
        extracted_dict_list = [
            {
                "ip": "219.74.230.75",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "PUT",
                "path": "/static/js/app.js",
                "protocol": "HTTP/1.1",
                "status": 404,
                "size": 761
            },
            {
                "ip": "156.184.109.43",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "GET",
                "path": "/contact",
                "protocol": "HTTP/1.1",
                "status": 401,
                "size": 545
            },
            {
                "ip": "39.243.78.244",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "POST",
                "path": "/products",
                "protocol": "HTTP/1.1",
                "status": 500,
                "size": 1744
            },
            {
                "ip": "10.43.107.180",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "POST",
                "path": "/",
                "protocol": "HTTP/1.1",
                "status": 201,
                "size": 1891
            },
            {
                "ip": "166.85.221.59",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "GET",
                "path": "/login",
                "protocol": "HTTP/1.1",
                "status": 301,
                "size": 4520
            }
        ]
        self.assertEqual(result, extracted_dict_list)
    
    def test_extracted_data_from_loggly_json_format_file(self):
        result = extract_data_from_file("3", "/Users/danielhall/Desktop/Automation/Python Scripts/tests/access_log_analyzer_test.py")
        extracted_dict_list = [
            {
                "timestamp": "2025-08-29T00:37:02.242229",
                "ip": "31.132.45.182",
                "method": "GET",
                "path": "/contact",
                "status": 401,
                "size": 6375,
                "response_time_ms": 235,
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
                "host": "server3.prod.local",
                "env": "staging",
                "request_id": "req-351052"
            },
            {
                "timestamp": "2025-08-29T00:37:02.242280",
                "ip": "108.170.107.21",
                "method": "PUT",
                "path": "/",
                "status": 200,
                "size": 6151,
                "response_time_ms": 360,
                "user_agent": "curl/7.68.0",
                "host": "server4.prod.local",
                "env": "staging",
                "request_id": "req-897416"
            },
            {
                "timestamp": "2025-08-29T00:37:02.242312",
                "ip": "185.241.80.168",
                "method": "DELETE",
                "path": "/favicon.ico",
                "status": 301,
                "size": 6649,
                "response_time_ms": 432,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/113.0 Safari/537.36",
                "host": "server4.prod.local",
                "env": "staging",
                "request_id": "req-658389"
            },
            {
                "timestamp": "2025-08-29T00:37:02.242349",
                "ip": "17.33.169.147",
                "method": "PUT",
                "path": "/index.html",
                "status": 301,
                "size": 974,
                "response_time_ms": 365,
                "user_agent": "Wget/1.20.3 (linux-gnu)",
                "host": "server4.prod.local",
                "env": "dev",
                "request_id": "req-908069"
            },
            {
                "timestamp": "2025-08-29T00:37:02.242382",
                "ip": "95.27.207.11",
                "method": "PUT",
                "path": "/contact",
                "status": 302,
                "size": 8372,
                "response_time_ms": 79,
                "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Firefox/113.0",
                "host": "server5.prod.local",
                "env": "dev",
                "request_id": "req-537665"
            }
        ]
        self.assertEqual(result, extracted_dict_list)
    
    def test_extracted_data_from_apache_combined_format_file(self):
        result = extract_data_from_file("4", "/Users/danielhall/Desktop/Automation/Python Scripts/tests/access_log_analyzer_test.py")
        extracted_data_list = [
            {
                "ip": "127.167.171.1",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "GET",
                "path": "/dashboard",
                "protocol": "HTTP/1.1",
                "status": 404,
                "size": 7317,
                "referer": "-",
                "user_agent": "curl/7.68.0"
            },
            {
                "ip": "117.74.190.180",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "DELETE",
                "path": "/products",
                "protocol": "HTTP/1.1",
                "status": 500,
                "size": 2803,
                "referer": "-",
                "user_agent": "Wget/1.20.3 (linux-gnu)"
            },
            {
                "ip": "207.238.22.214",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "POST",
                "path": "/static/js/app.js",
                "protocol": "HTTP/1.1",
                "status": 404,
                "size": 4086,
                "referer": "-",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15"
            },
            {
                "ip": "41.177.11.204",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "POST",
                "path": "/dashboard",
                "protocol": "HTTP/1.1",
                "status": 503,
                "size": 2195,
                "referer": "-",
                "user_agent": "Wget/1.20.3 (linux-gnu)"
            },
            {
                "ip": "182.218.163.134",
                "timestamp": "29/Aug/2025:00:37:02",
                "method": "DELETE",
                "path": "/dashboard",
                "protocol": "HTTP/1.1",
                "status": 502,
                "size": 2418,
                "referer": "-",
                "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Firefox/113.0"
            }
        ]
        self.assertEqual(result, extracted_data_list)

'''
    def test_total_number_of_requests(self):
        result = total_number_of_requests([{},{}])
        self.assertEqual(result, "")

    def test_IP_frequencies(self):
        result = IP_frequencies([{},{}])
        self.asserEqual(result, "")

    def test_status_code_destribution(self):
        result = status_code_destribution([{},{}])
        self.assertEqual(result, "")

    def test_error_percentage(self):
        result = error_percentage([{}])
        self.assertEqual(result, "")

    def test_hourly_traffics(self):
        result = hourly_traffics([{}])
        self.assertEqual(result, "")

    def test_hourly_traffics(all_data_dict_list):
'''

if __name__ == "__main__":
    unittest.main()
