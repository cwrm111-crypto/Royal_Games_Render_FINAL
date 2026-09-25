import json
class ConfigLoader:
    def load(self, path):
        with open(path,encoding='utf-8') as f: return json.load(f)
