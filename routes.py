from aiohttp import web
from test_module import test_module
import asyncio


def setup_route(app):
    app.router.add_get('/response/text/{u}/{p}', responseText)
    app.router.add_get('/response/body/{u}/{p}', responseBody)
    app.router.add_get('/response/json', responseJson)
    app.router.add_get('/r', redirect)


@asyncio.coroutine
def responseText(rq):
    userKey =  rq.match_info.get("u") or 'x'
    productKey =  rq.match_info.get("p") or 'x'

    size = str(test_module(userInfo, productInfo))

    return  web.Response(text= size)


@asyncio.coroutine
def responseBody(rq):
    return web.Response(body=b"Hello, world")


@asyncio.coroutine
def responseJson(rq):
    data = {'some': 'data'}
    return web.json_response(data)


@asyncio.coroutine
def redirect(request):
    return web.HTTPFound('/response/json')
