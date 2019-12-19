#!/usr/bin/env python
# coding=utf-8

import unittest
import json

import pathmagic

from base import BaseTestClass


class TestCustomer(BaseTestClass):
    'Test User'

    def test_dummy_endpoin(self):
        '''
        Check if the dummy function works.
        '''
        res = self.tester_app.get('/customers/dummy')

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data(as_text=True))
        self.assertEqual(data, 'Hello!')


if __name__ == '__main__':
    unittest.main()
