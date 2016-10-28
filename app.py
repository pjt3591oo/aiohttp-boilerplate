import asyncio
import logging
from aiohttp import web

from routes import setup_route as setup_route
from middleware import setup_middlewares

import configure.conf as conf

def __init__(loop):

    app = web.Application(loop=loop)

    host = conf.server["host"]
    port = conf.server["port"]

    setup_route(app)
    setup_middlewares(app)

    return app, host, port


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = __init__(loop)

    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    print(conf.server["message"])
    main()
