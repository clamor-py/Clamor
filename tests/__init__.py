# -*- coding: utf-8 -*-

import os
import sys
import unittest.runner

_dir = os.path.dirname(__file__)


def suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(_dir, 'test_*.py')

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    result = runner.run(suite())

    sys.exit(not result.wasSuccessful())
