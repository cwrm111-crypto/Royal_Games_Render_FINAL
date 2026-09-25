class XPService:
    def add(self, profile, amount):
        profile['xp']=profile.get('xp',0)+max(0,int(amount))
        profile['level']=1+profile['xp']//100
        return profile
