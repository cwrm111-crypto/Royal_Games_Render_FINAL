def handle(payload=None):
    return {'ok': True, 'route': 'health', 'payload': payload or {}}
