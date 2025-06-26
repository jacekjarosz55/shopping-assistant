import unittest

if __name__ == "__main__":
    test_loader = unittest.TestLoader()

    # Discover both unit and integration tests
    unit_tests = test_loader.discover("tests", pattern="test_*.py")
    integration_tests = test_loader.discover(
        "tests/integration", pattern="test_*.py"
    )

    test_suite = unittest.TestSuite([unit_tests, integration_tests])
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
