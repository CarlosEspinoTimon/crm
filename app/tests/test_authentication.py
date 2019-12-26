#!/usr/bin/env python
# coding=utf-8

import unittest
import json

import pathmagic

from base import BaseTestClass


class TestAuthentication(BaseTestClass):
    'Test Authentication'

    def test_login(self):
        self.create_user()

        res = self.tester_app.post(
            '/login',
            headers={
                'Content-Type': 'application/json',
                'email': 'user@email.com',
                'password': '1234'
            })
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertTrue('Token: ' in data)


if __name__ == '__main__':
    unittest.main()
