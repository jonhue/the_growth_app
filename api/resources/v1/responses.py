def respond(code=200, payload={}, messages=[]):
    return {
        'status': 'ok' if int(code/100) == 2 else 'error',
        'code': code,
        'messages': messages,
        'payload': payload,
    }, code
