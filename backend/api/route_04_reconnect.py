def handle(payload=None):
    return {'ok': True, 'route': 'reconnect', 'payload': payload or {}}
