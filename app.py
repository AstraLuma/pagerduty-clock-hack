from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse('Hello, world!')


async def startup():
    print('Ready to go')


async def pdhook(request):
    event = await request.json()
    return JSONResponse({'event': event})


routes = [
    Route('/', homepage),
    Route('/webhook/pagerduty/{ident}', pdhook, methods=['POST']),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
