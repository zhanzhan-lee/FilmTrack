# tests/test_unit_auth.py

import unittest
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        print("\nSetting up test environment")
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.user = User(username='testuser')
        self.user.set_password('password')
        db.session.add(self.user)
        db.session.commit()
        print("Test user created and logged in")

    def tearDown(self):
        print("Tearing down test environment")
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_register_success(self):
        print("Testing register success")
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpassword',
            'confirm_password': 'newpassword',
            'agree_terms': 'y',
            'agree_policy': 'y',
            'subscribe': 'y'
        }, follow_redirects=True)
        self.assertIn(b'Registration successful', response.data)
        print("Register success test passed")

    def test_register_existing_user(self):
        print("Testing register with existing username")
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'somepassword',
            'confirm_password': 'somepassword',
            'agree_terms': 'y',
            'agree_policy': 'y'
        }, follow_redirects=True)
        self.assertIn(b'Username already exists', response.data)
        print("Register existing user test passed")

    def test_login_success(self):
        print("Testing login success")
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)
        self.assertIn(b'Welcome, testuser', response.data)
        print("Login success test passed")

    def test_login_fail(self):
        print("Testing login fail")
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b'Login failed', response.data)
        print("Login fail test passed")

    def test_logout(self):
        print("Testing logout")
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'Login', response.data)
            print("Logout test passed")

    def test_profile_requires_login(self):
        print("Testing access to profile without login")
        response = self.client.get('/profile', follow_redirects=True)
        self.assertIn(b'Login', response.data)
        print("Profile requires login test passed")

    def test_profile_access(self):
        print("Testing access to profile after login")
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password'}, follow_redirects=True)
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Profile', response.data)
            print("Profile access test passed")
