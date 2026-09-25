class SupportAI:
    def reply(self, text):
        t=text.lower()
        if 'wallet' in t: return 'আপনার virtual coin balance Wallet থেকে দেখুন।'
        if 'game' in t: return 'Play থেকে একটি available game room নির্বাচন করুন।'
        return 'আমি Royal Games support assistant। আপনার প্রশ্নটি সংক্ষেপে লিখুন।'
