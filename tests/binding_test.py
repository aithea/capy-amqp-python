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
                pass

            def on_finalize(self):
                pass

        broker = capy_amqp\
            .bind("amqp://guest:guest@localhost:5672/")\
            .run(capy_amqp.Launch.async)

        handler = Fetcher()

        for i in range(0, 100):
            action = dict({
                'action':  'echo',
                'payload': {"ids": int(time.time()), "timestamp": int(time.time()), "i": i},
                'users': [{1: '1'}, {2: '2'}, {3: '3'}]
            })

            broker\
                .fetch(action, "echo.ping", handler)

        time.sleep(1)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
