class AchievementService:
    RULES={'first_win':lambda s:s.get('wins',0)>=1,'ten_wins':lambda s:s.get('wins',0)>=10}
    def earned(self, stats): return [k for k,f in self.RULES.items() if f(stats)]
