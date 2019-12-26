#!/usr/bin/env python
# coding=utf-8

from test_server import *
from test_customer import *
from test_authentication import *

import unittest
import pathmagic

from server import create_app


if __name__ == '__main__':
    unittest.main()
