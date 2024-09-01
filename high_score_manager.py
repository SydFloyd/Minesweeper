class HighScoreManager:
    def __init__(self, persistence_manager, max_high_scores=10):
        self.persistence_manager = persistence_manager
        self.max_high_scores = max_high_scores
        self.high_scores_key = 'high_scores'
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        """Loads the high scores from the persistence manager."""
        return self.persistence_manager.get_data(self.high_scores_key, {"Easy": [], "Medium": [], "Hard": []})

    def save_high_scores(self):
        """Saves the current high scores to the persistence manager."""
        self.persistence_manager.set_data(self.high_scores_key, self.high_scores)

    def add_high_score(self, level, name, time):
        """Adds a new high score, sorts the list by score and time, and limits the list size."""
        if level not in self.high_scores:
            self.high_scores[level] = []
        self.high_scores[level].append({'name': name, 'time': time})
        self.high_scores[level] = sorted(self.high_scores[level], key=lambda x: x['time'])

        # Limit the number of high scores stored
        if len(self.high_scores[level]) > self.max_high_scores:
            self.high_scores[level] = self.high_scores[level][:self.max_high_scores]

        self.save_high_scores()

    def get_high_scores(self, level):
        """Returns the list of high scores."""
        return self.high_scores[level]
    
    def get_high_score_time(self, level):
        """Returns the highest score."""
        return max(score['time'] for score in self.high_scores[level])
