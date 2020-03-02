import json

import logging

from marshmallow import Schema, ValidationError

from .request import Request
from .client import Client
from .jsonrpc import jrpc_accept, jrpc_response, validate_jrpc_request
from .errors import (
    CorvusException, NotFound, UnknownAsgiAction, ParseError, InvalidRequest,
    Unauthorized
)


class App:

    def __init__(
        self, title = 'Another Corvus App',
        version = '0.0.1', *args, **kwargs
    ):

        self.title = title
        self.version = version
        self.methods = {}
        self.clients = {}
        self.users = {}
        self.hooks = {
            'before_startup': None,
            'after_startup': None,
            'before_shutdown': None,
            'after_shutdown': None,
            'before_connection': None,
            'after_connection': None,
            'on_disconnection': None,
            'on_request': None,
            'on_response': None
        }
        self.args = args
        self.kwargs = kwargs

        logging.info(f'{self.title} [{self.version}] inited')

    def _run_hook(self, hook_name, *args):

        if not self.hooks[hook_name]:
            return

        self.hooks[hook_name](app=self, *args)

    def add_hook(self, hook_name, hook_func):

        if hook_name not in self.hooks.keys():
            logging.error(f'Unknown hook {hook_name}')
            return

        self.hooks[hook_name] = hook_func

    def _init_client(self, base_request, send):

        client = Client(base_request, send)
        self.clients[base_request.ws_id] = client

        return client

    def _remove_client(self, client):
        self.clients.pop(client.ws_id)

    def _make_request(self, base_request, message):

        try:
            parsed = json.loads(message['text'])
        except json.JSONDecodeError:
            raise ParseError

        if not validate_jrpc_request(parsed):
            raise InvalidRequest

        if parsed['method'] not in self.methods.keys():
            raise NotFound

        return base_request._make_request(parsed)

    async def _make_response(self, request, client):
        return await self.methods[request.method](request, client)

    def add_method(self, name, method):
        self.methods[name] = method

    def method(self, name):

        def wrapped(method):

            self.methods[name] = method
            return method

        return wrapped

    def add_user(self, client, user):

        client.user = user
        self.users[user.id] = client

    def remove_user(self, client):
        self.users.pop(client.user.id)

    def before(self, func):
        def decorator(method):
            async def wrapped(req, client):

                req, client = func(req, client)
                return await method(req, client)
            return wrapped
        return decorator

    def after(self, func):
        def decorator(method):
            async def wrapped(req, client):

                resp = await method(req, client)
                return func(req, resp, client)
            return wrapped
        return decorator

    def user_required(self, method):

        async def wrapped(req, client):

            if not client.user:
                raise Unauthorized
            return await method(req, client)

        return wrapped

    async def __call__(self, scope, receive, send):

        if scope['type'] == 'lifespan':

            message = await receive()

            if message['type'] == 'lifespan.startup':

                self._run_hook('before_startup', scope, receive, send)
                await send({'type': 'lifespan.startup.complete'})
                self._run_hook('after_startup', scope, receive, send)
                return

            elif message['type'] == 'lifespan.shutdown':

                self._run_hook('before_shutdown', scope, receive, send)
                await send({'type': 'lifespan.shutdown.complete'})
                self._run_hook('after_shutdown', scope, receive, send)
                return

        elif scope['type'] == 'websocket':
            pass

        else:
            logging.error(f"Unsupported scope type - {scope['type']}")
            return

        message = await receive()

        if message['type'] == 'websocket.connect':
            self._run_hook('before_connection', scope, receive, send, message)
        else:
            return

        await send(jrpc_accept())
        self._run_hook('after_connection', scope, receive, send)

        base_request = Request(scope, receive, send)
        client = self._init_client(base_request, send)

        while True:

            message = await receive()

            if message['type'] in ('websocket.disconnect', 'websocket.close'):
                self._run_hook('on_disconnection', message, client)
                break

            elif message['type'] == 'websocket.receive':

                try:
                    request = self._make_request(base_request, message)
                except CorvusException as e:
                    await send(e.error())
                    continue

                self._run_hook('on_request', request, client)

                try:
                    response = await self._make_response(request, client)
                except CorvusException as e:
                    await send(e.error())
                    continue

                self._run_hook('on_response', response, client)

                if response:
                    await send(jrpc_response(response, request.id))

            else:
                await send(UnknownAsgiAction.error())

        self._remove_client(client)
