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

    # Ensure that correct login works
    def test_login_good_creds(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertTrue(b'Welcome! You are now logged in.' in response.data)

    # Ensure that bad login fails
    def test_login_bad_creds(self):
        tester = app.test_client(self)
        response = tester.post(
        '/login',
        data=dict(username="kara", password="arlene"),
        follow_redirects=True
        )
        self.assertTrue(b'Invalid Credentials. Please try again.' in response.data)

    # Ensure that logout passes
    def test_logout_page_load(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'You are now logged out. Thanks for reading!' in response.data)

    # Ensure that main page requires log in
    def test_login_test_main(self):
        tester = app.test_client()
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'Please log in.' in response.data)

    # Ensure that logout page requires log in
    def test_login_test_logout(self):
        tester = app.test_client()
        response = tester.get('/logout', follow_redirects=True)
        self.assertTrue(b'Please log in.' in response.data)

    # Ensure that spots are displayed
    def test_spot_display(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertTrue(b'Burger King' in response.data)


if __name__ == '__main__':
    unittest.main()