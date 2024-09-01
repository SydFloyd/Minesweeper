import time

class Timer:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def start(self):
        """Start the timer."""
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.event_manager.dispatch('timer_started')
            self._update_timer()

    def stop(self):
        """Stop the timer."""
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False
            self.event_manager.dispatch('timer_stopped', self.elapsed_time)

    def reset(self):
        """Reset the timer."""
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self.event_manager.dispatch('timer_reset')

    def get_elapsed_time(self):
        """Get the total elapsed time since the timer started."""
        if self.running:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time

    def _update_timer(self):
        """Private method to update the timer every second."""
        if self.running:
            # Dispatch event to update the timer UI
            self.event_manager.dispatch('timer_updated')
            # Schedule the next update after 1 second
            self.event_manager.root.after(1000, self._update_timer)
