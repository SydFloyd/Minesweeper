class SettingsManager:
    def __init__(self):
        self.levels = {
            "Easy": {"grid_size": (9, 9), "num_mines": 10, "window_size": "410x405"},
            "Medium": {"grid_size": (16, 16), "num_mines": 40, "window_size": "735x700"},
            "Hard": {"grid_size": (16, 30), "num_mines": 99, "window_size": "1375x700"}
        }
        self.active_level = "Medium"  # Default

    def get_setting(self, setting_name):
        return self.levels[self.active_level][setting_name]

    def set_active_level(self, level_name):
        level_lookup = {"E": "Easy", "M": "Medium", "H": "Hard"}
        level_name = level_lookup.get(level_name, level_name)
        if level_name in self.levels:
            self.active_level = level_name

    def get_active_level(self):
        return self.active_level
    