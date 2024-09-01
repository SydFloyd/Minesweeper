class SettingsManager:
    def __init__(self, persistence_manager):
        # - **Standard Levels**: There are three standard levels in Minesweeper:
        # - **Beginner**: 8x8 grid with 10 mines.
        # - **Intermediate**: 16x16 grid with 40 mines.
        # - **Expert**: 30x16 grid with 99 mines.
        self.persistence_manager = persistence_manager
        self.default_settings = {
            'grid_size': (10, 10),   # Default grid size (rows, cols)
            'num_mines': 20,         # Default number of mines
            'theme': 'light',        # Default theme (light/dark)
            'window_size': '460x450'
        }
        self.settings = self._load_settings()

    def _load_settings(self):
        """Loads settings from the persistence manager or uses default settings."""
        return {key: self.persistence_manager.get_data(key, default_value)
                for key, default_value in self.default_settings.items()}

    def save_settings(self):
        """Saves the current settings to the persistence manager."""
        for key, value in self.settings.items():
            self.persistence_manager.set_data(key, value)

    def get_setting(self, key):
        """Retrieves the value of a specific setting."""
        return self.settings.get(key, self.default_settings.get(key))

    def set_setting(self, key, value):
        """Sets a specific setting and saves it."""
        self.settings[key] = value
        self.save_settings()

    def reset_to_defaults(self):
        """Resets all settings to their default values."""
        self.settings = self.default_settings.copy()
        self.save_settings()

    def delete_setting(self, key):
        """Deletes a specific setting and reverts it to default."""
        if key in self.settings:
            del self.settings[key]
            self.persistence_manager.delete_data(key)
            self.settings[key] = self.default_settings.get(key)
