#!/usr/bin/env python
# coding=utf-8

import unittest

import pathmagic

from server import create_app


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.Test')
        self.tester_app = self.app.test_client()
