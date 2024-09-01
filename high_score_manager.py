class HighScoreManager:
    def __init__(self, persistence_manager, max_high_scores=10):
        self.persistence_manager = persistence_manager
        self.max_high_scores = max_high_scores
        self.high_scores_key = 'high_scores'
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        """Loads the high scores from the persistence manager."""
        return self.persistence_manager.get_data(self.high_scores_key, [])

    def save_high_scores(self):
        """Saves the current high scores to the persistence manager."""
        self.persistence_manager.set_data(self.high_scores_key, self.high_scores)

    def add_high_score(self, name, time):
        """Adds a new high score, sorts the list by score and time, and limits the list size."""
        new_score = {'name': name, 'time': time}
        self.high_scores.append(new_score)
        self.high_scores = sorted(self.high_scores, key=lambda x: x['time'])

        # Limit the number of high scores stored
        if len(self.high_scores) > self.max_high_scores:
            self.high_scores = self.high_scores[:self.max_high_scores]

        self.save_high_scores()

    def get_high_scores(self):
        """Returns the list of high scores."""
        return self.high_scores
    
    def get_high_score_time(self):
        """Returns the highest score."""
        return max(score['time'] for score in self.high_scores)

    def clear_high_scores(self):
        """Clears all high scores."""
        self.high_scores = []
        self.save_high_scores()

