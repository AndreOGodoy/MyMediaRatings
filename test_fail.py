import unittest

class TestsTest(unittest.TestCase):

    def test_should_fail(self):
       self.assertTrue(False)

    def test_should_pass(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
