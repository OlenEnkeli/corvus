from .utils import proccess_headers
from .jsonrpc import jrpc_response


class Client:

    def __init__(self, base_request, send):

        self._send = send
        self._base_request = base_request
        self.ws_id = base_request.ws_id

        self.user = None

    def __repr__(self):
        return f'<Client: {self.ws_id}>'

    def __str__(self):
        return self.__repr__()

    async def send(self, data):
        await self._send(jrpc_response(data))
