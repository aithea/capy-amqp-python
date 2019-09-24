import unittest
import time
import capy_amqp


class MyTestCase(unittest.TestCase):
    def test_something(self):

        class Fetcher(capy_amqp.FetchHandler):

            def on_data(self, data):
                print(data)

            def on_error(self, code, message):
                print(code, message)

            def on_success(self):
                print("on success")

            def on_finalize(self):
                print("on finalize")

        broker = capy_amqp\
            .Bind("amqp://guest:guest@localhost:5672/")\
            .run()

        action = dict({
            'action':  'echo',
            'payload': {"ids": int(time.time()), "timestamp": int(time.time()), "i": 0}
        })

        handler = Fetcher()

        broker\
            .fetch(action, "echo.ping", handler)

        time.sleep(1)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
