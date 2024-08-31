# Assuming you have a test framework like unittest

import unittest
from timer import Timer
from event_manager import EventManager
import time

class TestTimer(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager()
        self.timer = Timer(self.event_manager)

    def test_timer_start(self):
        self.timer.start()
        self.assertTrue(self.timer.running)
        self.assertIsNotNone(self.timer.start_time)

    def test_timer_stop(self):
        self.timer.start()
        time.sleep(1)  # Simulate some elapsed time
        self.timer.stop()
        self.assertFalse(self.timer.running)
        self.assertGreater(self.timer.elapsed_time, 0)

    def test_timer_reset(self):
        self.timer.start()
        time.sleep(1)
        self.timer.stop()
        self.timer.reset()
        self.assertEqual(self.timer.elapsed_time, 0)
        self.assertFalse(self.timer.running)

    def test_timer_events(self):
        events = []
        self.event_manager.subscribe('timer_started', lambda: events.append('started'))
        self.event_manager.subscribe('timer_stopped', lambda time: events.append('stopped'))
        self.event_manager.subscribe('timer_reset', lambda: events.append('reset'))

        self.timer.start()
        self.timer.stop()
        self.timer.reset()

        self.assertListEqual(events, ['started', 'stopped', 'reset'])

if __name__ == '__main__':
    unittest.main()
