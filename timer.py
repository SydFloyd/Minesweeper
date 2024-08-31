import time

class Timer:
    def __init__(self, event_manager):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self.event_manager = event_manager

        # Subscribe to the event to start the timer
        self.event_manager.subscribe('start_timer', self.start)

    def start(self):
        """Starts the timer."""
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.event_manager.dispatch('timer_started')

    def stop(self):
        """Stops the timer and calculates the elapsed time."""
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False
            self.event_manager.dispatch('timer_stopped', self.elapsed_time)

    def reset(self):
        """Resets the timer to 0 and stops it."""
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self.event_manager.dispatch('timer_reset')

    def get_elapsed_time(self):
        """Returns the elapsed time in seconds."""
        if self.running:
            return time.time() - self.start_time
        return self.elapsed_time
