import unittest
import capy_amqp


class MyTestCase(unittest.TestCase):
    def test_something(self):

        class Listener(capy_amqp.ListenHandler):

            index = 0

            def on_data(self, request, routing_key):
                print(request, routing_key)
                self.index += 1
                return {"response": True, "index": self.index, 'users': [{1: '1'}, {2: '1'}, {3: '3'}]}

            def on_error(self, code, message):
                print(code, message)

            def on_success(self):
                pass

            def on_finalize(self):
                pass

        handler = Listener()

        while True:

            capy_amqp \
                .bind("amqp://guest:guest@localhost:5672/")\
                .listen("capy-test", ["echo.ping"], handler)\
                .run(capy_amqp.Launch.sync)

            self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
