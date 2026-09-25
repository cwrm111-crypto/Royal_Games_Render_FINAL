from dataclasses import dataclass, field
from collections import defaultdict
@dataclass
class Queue:
    players: list[str] = field(default_factory=list)
class Matchmaker:
    def __init__(self): self.queues=defaultdict(Queue)
    def join(self, game:str, player_id:str): 
        if player_id not in self.queues[game].players: self.queues[game].players.append(player_id)
        return list(self.queues[game].players)
    def pop_match(self, game:str, size:int=2):
        q=self.queues[game].players
        if len(q)<size: return None
        match=q[:size]; del q[:size]; return match
