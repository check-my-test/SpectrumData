import unittest
from unittest import TestSuite

import coverage


def load_tests(loader, tests, pattern):
    """Запускает все тесты в директории ``./tests/``, которые начинаются на ``test_*.py``"""
    suite = TestSuite()
    for all_test_suite in unittest.defaultTestLoader.discover("./tests/", "test_*.py"):
        for test_suite in all_test_suite:
            # print("test_suite", test_suite._exception)
            suite.addTests(test_suite)
    return suite


if __name__ == "__main__":
    cov = coverage.Coverage()
    cov.start()

    unittest.main(exit=False)

    cov.stop()
    cov.save()
    cov.report()
    cov.html_report()
