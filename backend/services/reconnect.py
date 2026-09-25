class ReconnectRegistry:
    def __init__(self): self.sessions={}
    def bind(self, player_id, room_id): self.sessions[str(player_id)]=room_id
    def room_for(self, player_id): return self.sessions.get(str(player_id))
    def unbind(self, player_id): self.sessions.pop(str(player_id), None)
