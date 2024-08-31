class EventManager:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name, listener):
        """Subscribe a listener to an event."""
        self.listeners.setdefault(event_name, []).append(listener)

    def dispatch(self, event_name, *args, **kwargs):
        """Dispatch an event to all its listeners."""
        for listener in self.listeners.get(event_name, []):
            listener(*args, **kwargs)
