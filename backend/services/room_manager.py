class RoomManager:
    def __init__(self): self.rooms={}
    def create(self, room_id, game): self.rooms[room_id]={'game':game,'players':[]}; return self.rooms[room_id]
    def add(self, room_id, player): self.rooms[room_id]['players'].append(player)
    def get(self, room_id): return self.rooms.get(room_id)
    def remove(self, room_id): self.rooms.pop(room_id, None)
