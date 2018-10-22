import unittest
from spotmanager import app

class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that login shows correctly
    def test_login_page_load(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        self.assertTrue(b'Hello! Please log in.' in response.data) 

if __name__ == '__main__':
    unittest.main()