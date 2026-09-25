from datetime import datetime, timedelta
from backend import db
class TournamentService:
    def list(self):
        return [
          {"id":1,"title":"Daily Teen Patti","game_type":"TEEN_PATTI","entry_fee":0,"prize_pool":5000,"max_players":100,"status":"LIVE"},
          {"id":2,"title":"Weekend Multi-Game","game_type":"RUMMY","entry_fee":0,"prize_pool":10000,"max_players":200,"status":"UPCOMING"}
        ]
