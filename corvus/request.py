from copy import copy

from .utils import proccess_headers


class Request:

    def __init__(self, scope, receive, send):

        self._scope = scope
        self._receive = receive
        self._send = send

        self.headers = proccess_headers(scope['headers'])
        self.ws_id = self.headers['sec-websocket-key']

        self.id = None
        self.method = None
        self.data = None

    def __repr__(self):
        return f'<Request: {self.id}>'

    def __str__(self):
        return self.__repr__()

    def _make_request(self, data):

        request = copy(self)
        request.id = data['id']
        request.method = data['method']
        request.data = data['params']

        return request
