class Bracket:
    def build(self, players):
        players=list(players); return [(players[i], players[i+1]) for i in range(0,len(players)-1,2)]
