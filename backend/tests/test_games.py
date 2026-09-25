from backend.games.teen_patti import _eval,TeenPatti,compare
def c(v,s="♠"): return {"rank":str(v),"suit":s,"value":v}
def test_trail(): assert _eval([c(9),c(9,"♥"),c(9,"♦")])[0]==TeenPatti.TRAIL
def test_sequence(): assert _eval([c(5),c(4,"♥"),c(3,"♦")])[0]==TeenPatti.SEQUENCE
def test_pure(): assert _eval([c(10),c(9),c(8)])[0]==TeenPatti.PURE_SEQUENCE
def test_compare(): assert compare([c(10),c(10,"♥"),c(10,"♦")],[c(9),c(9,"♥"),c(9,"♦")])>0
