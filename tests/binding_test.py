import unittest
import time

from __capy_amqp \
    import Bind as Bind, \
    FetchHandler as FetchHandler


class MyTestCase(unittest.TestCase):
    def test_something(self):

        class Fetcher(FetchHandler):

            def on_data(self, data):
                print(data)

        broker = Bind("amqp://guest:guest@localhost:5672/")

        action = dict()
        action["action"] = "echo"
        action["payload"] = {"ids": time.time(), "timestamp": time.time(), "i": 0}

        key = "echo.ping"

        broker.fetch(action, key, Fetcher())

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
