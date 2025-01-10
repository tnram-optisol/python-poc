import unittest

import module1


class TestModule1(unittest.TestCase):
    def test_module_should_return_value(self):
        user = ['script.py', '--name', 'John', '--age', '20']
        result = module1.parse_data(user)
        self.assertEqual(result, {'name': 'John', 'age': '20'})

    def test_module_should_return2(self):
        user = ['script.py', '--name', 'John']
        result = module1.parse_data(user)
        self.assertEqual(result, {'name': 'John'})

    def test_module_should_fail(self):
        user = ['script.py']
        result = module1.parse_data(user)
        self.assertEqual(result, 'Check input or use --help')


if __name__ == "__main__":
    unittest.main()
