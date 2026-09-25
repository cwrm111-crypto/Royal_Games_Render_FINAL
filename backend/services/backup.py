import json, pathlib, datetime
class JsonBackup:
    def dump(self, path, data):
        p=pathlib.Path(path); p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        return str(p)
