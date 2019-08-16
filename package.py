import json

def _unpack(data):
    return json.loads(data)

def _pack(data):
    data = json.dumps(data)
    return bytes(data,'utf-8')



