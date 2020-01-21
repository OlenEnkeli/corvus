from functools import partial

from .jsonrpc import jrpc_error


class CorvusException(Exception):
    pass


class NotFound(CorvusException):
    error = partial(jrpc_error, -32601, 'Method not found')


class ParseError(CorvusException):
    error = partial(jrpc_error, -32700, 'Parse error')


class InvalidRequest(CorvusException):
    error = partial(jrpc_error, -32600, 'Invalid Request')


class InvalidParams(CorvusException):
    error = partial(jrpc_error, -32602, 'Invalid params')


class InternalError(CorvusException):
    error = partial(jrpc_error, -32603, 'Internal error')


class UnknownAsgiAction(CorvusException):
    error = partial(jrpc_error, -31000, 'Unknown ASGI action recived')


class Unauthorized(CorvusException):
    error = partial(jrpc_error, -32000, 'Unauthorized')
