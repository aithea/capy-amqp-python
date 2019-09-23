import unittest
from __capy_amqp import __open as amqp_open


class MyTestCase(unittest.TestCase):
    def test_something(self):
        map = amqp_open("...")
        print("map: ", map)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
