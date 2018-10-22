import os

from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from settings import key
import unittest

app = Flask(__name__)

class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that login shows correctly
    def test_login_page_load(self):
        tester = app.test_client(self)
        self.assertTrue('Hello! Please log in.' in response.data)

if __name__ == '__main__':
    unittest.main()