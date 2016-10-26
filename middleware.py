import aiohttp_jinja2
from aiohttp import web
from log import success_log, error_log, critical_log
import logging


#잘못요청
async def handle_404(request, response):
    user = request.match_info.get("userKey") or 'x'
    product = request.match_info.get("productKey") or 'x'

    error_log(user, product, "404")

    raise web.HTTPNotFound()


#서버에러
async def handle_500(request, response):
    user = request.match_info.get("userKey") or 'x'
    product = request.match_info.get("productKey") or 'x'

    critical_log(user,product,"500")

    return response


#성공적으로 처리
async def handle_200(request, response):
    user = request.match_info.get("userKey") or 'x'
    product = request.match_info.get("productKey") or 'x'
    recommend = response.text or 'x'

    success_log(user, product, recommend)

    return response


def error_pages(overrides):
    async def middleware(app, handler):
        async def middleware_handler(request):
            try:
                response = await handler(request)
                override = overrides.get(response.status)
                if override is None:
                    return response
                else:
                    return await override(request, response)
            except web.HTTPException as ex:
                override = overrides.get(ex.status)
                if override is None:
                    raise
                else:
                    return await override(request, ex)
        return middleware_handler
    return middleware


def setup_middlewares(app):
    error_middleware = error_pages({404: handle_404,
                                    500: handle_500,
                                    200: handle_200
                                    })
    app.middlewares.append(error_middleware)
