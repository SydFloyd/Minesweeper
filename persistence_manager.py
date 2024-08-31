import json
import os

class PersistenceManager:
    def __init__(self, storage_file='game_data.json'):
        self.storage_file = storage_file
        self.data = self._load_data()

    def _load_data(self):
        """Loads data from the storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as file:
                    return json.load(file)
            except (IOError, json.JSONDecodeError):
                pass
        return {}

    def save_data(self):
        """Saves the current data to the storage file."""
        try:
            with open(self.storage_file, 'w') as file:
                json.dump(self.data, file, indent=4)
        except IOError as e:
            print(f"An error occurred while saving data: {e}")

    def get_data(self, key, default=None):
        """Retrieves the value for the given key from the data."""
        return self.data.get(key, default)

    def set_data(self, key, value):
        """Sets the value for the given key in the data and saves it."""
        self.data[key] = value
        self.save_data()

    def delete_data(self, key):
        """Deletes the data associated with the given key and saves the file."""
        if key in self.data:
            del self.data[key]
            self.save_data()
