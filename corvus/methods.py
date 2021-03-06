from marshmallow import ValidationError

from .errors import ParseError, Unauthorized


def load_schema(schema):
    def decorator(method):
        async def wrapped(req, client):

            try:
                req.data = schema().load(req.data)
            except ValidationError:
                raise ParseError

            return await method(req, client)
        return wrapped
    return decorator


def user_required(method):

    async def wrapped(req, client):

        if not client.user:
            raise Unauthorized
        return await method(req, client)

    return wrapped