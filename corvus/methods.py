from .errors import ValidationError, ParseError


def load_schema(self, schema):
    def decorator(method):
        async def wrapped(req, client):

            try:
                req.data = schema().load(req.data)
            except ValidationError:
                raise ParseError

            return await method(req, client)
        return wrapped
    return decorator
