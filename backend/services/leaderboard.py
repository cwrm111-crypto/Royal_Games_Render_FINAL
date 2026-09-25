class Leaderboard:
    def rank(self, users, key='coins', limit=100):
        return sorted(users, key=lambda u:u.get(key,0), reverse=True)[:limit]
