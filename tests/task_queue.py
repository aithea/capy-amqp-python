import unittest
import capy_amqp
import time
import random

class MyTestCase(unittest.TestCase):
    def test_something(self):

        class Task(capy_amqp.TaskHandler):

            def process(self):
                print("Task ... ")
                time.sleep(random.randint(1,5)/10)

        task_queue = capy_amqp.task_queue(4)
        task = Task()

        for i in range(1, 10):
            task_queue.put(task)

        time.sleep(10)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
