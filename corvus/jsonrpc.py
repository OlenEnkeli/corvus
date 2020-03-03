import json


JRPS_REQUEST_FIELDS = ['jsonrpc', 'id', 'method', 'params']


def jrpc_accept(headers=None):

    return {
        'type': 'websocket.accept', 
        'headers': headers
    }


def jrpc_send(data=None):

    bytes_data = json.dumps(data) if isinstance(data, dict) else bytes(data)

    return {
        'type': 'websocket.send',
        'bytes': bytes_data
    }


def jrpc_error(code=-32000, message='Server error', request_id=None):

    return jrpc_send({
        'jsonrpc': '2.0',
        'id': request_id,
        'error': {
            'code': code,
            'message': message
        }
    })


def jrpc_response(result={}, request_id=0):

    return jrpc_send({
        'jsonrpc': '2.0',
        'id': request_id,
        'result': result
    })


def validate_jrpc_request(data):

    for key in JRPS_REQUEST_FIELDS:
        if key not in data.keys():
            return False

    if (
        not isinstance(data['id'], int) or
        not isinstance(data['method'], str) or
        not isinstance(data['params'], (list, dict)) or
        data['jsonrpc'] != '2.0' or
        not data['method']
    ):
        return False

    return True
