def handle(payload=None):
    return {'ok': True, 'route': 'metrics', 'payload': payload or {}}
