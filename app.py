import asyncio
import logging

from aiohttp import web
from routes import setup_route as setup_route
from middleware import setup_middlewares


def __init__(loop):

    app = web.Application(loop=loop)

    host = "localhost"
    port = 8282

    setup_route(app)
    setup_middlewares(app)

    return app, host, port


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = __init__(loop)

    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    print('server on')
    main()
