from app import app
import unittest

class FlastTestCase(unittest.TestCase):

    def test_index(self):
        # Ensure that flask was setup correctly
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page_load(self):
        # Ensure the login page load correctly
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    def  test_login_with_credentials(self):
        # Ensure login behaves correctly with correct credentials
        tester = app.test_client(self)
        payload= {"username":"admin", "password":"admin"}
        response = tester.post('/login', data=payload, follow_redirects=True)
        self.assertIn(b'You were just logged in!', response.data)

    def test_login_with_wrong_credentials(self):
        # Ensure login behaves correctly with wrong credentials
        tester = app.test_client(self)
        payload= {"username":"admin", "password":"admiN"}
        response = tester.post('/login', data=payload, follow_redirects=True)
        self.assertTrue(b'Invlaid credentials. Please try again' in response.data)

    def test_correct_logout(self):
        # Ensure logout behaves correctly
        tester = app.test_client(self)
        payload= {"username":"admin", "password":"admin"}
        tester.post('/login', data=payload, follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were just logged out!', response.data)

    def test_main_page_required_login(self):
        # Ensure that the main page requires login
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertIn(b'You need to logging in first!', response.data)

    def test_main_page_logout(self):
        # Ensure that the main page requires login
        tester = app.test_client(self)
        payload= {"username":"admin", "password":"admin"}
        tester.post('/login', data=payload, follow_redirects=True)
        tester.get('/', follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You were just logged out!', response.data)

    def test_posts_show_up(self):
        # Ensure that posts show in the main page
        tester = app.test_client(self)
        payload= {"username":"admin", "password":"admin"}
        response = tester.post('/login', data=payload, follow_redirects=True)
        self.assertTrue(b'Good' in response.data)


if __name__ == '__main__':
    unittest.main()
