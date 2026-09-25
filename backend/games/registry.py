from .teen_patti import TeenPattiGame
from .rummy import RummyGame
from .call_break import CallBreakGame
from .hazari import HazariGame
from .andar_bahar import AndarBaharGame
from .blackjack import BlackjackGame
from .ludo import LudoGame
from .snakes_ladders import SnakesLaddersGame
from .poker_style import PokerStyleGame
GAME_CLASSES={
"TEEN_PATTI":TeenPattiGame,"RUMMY":RummyGame,"CALL_BREAK":CallBreakGame,"HAZARI":HazariGame,
"ANDAR_BAHAR":AndarBaharGame,"BLACKJACK":BlackjackGame,"LUDO":LudoGame,
"SNAKES_LADDERS":SnakesLaddersGame,"POKER_STYLE":PokerStyleGame}
def new_game(game_type,room_id):
    cls=GAME_CLASSES.get(game_type); return cls(room_id) if cls else None
