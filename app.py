import logging

from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse
from starlette.routing import Route


LOG = logging.getLogger(__name__)

#: The User ID of the user. eg, the last component of https://acme.pagerduty.com/users/PTUXL6G
MY_ID = 'P5KJGS9'


# Incident status can be:
# triggered, acknowledged, resolved

class IncidentTracker:
    def __init__(self):
        self._incidents = {}
        self._active_count = 0

    async def update(self, incident):
        iid = incident['id']
        LOG.debug("Updating incident %s", iid)
        self._incidents[iid] = incident
        await self._count_my_actives()

    async def _count_my_actives(self):
        """
        Goes through the incidents, counts the active ones that are mine, and 
        potentially triggers additional actions.
        """
        incs = [
            i['id']
            for i in self._incidents.values()
            if i['status'] in ('triggered',)
            if any(a['id'] == MY_ID for a in i['assignees'])
        ]
        LOG.debug("Counted incidents: %r", incs)
        old_count = self._active_count
        new_count = len(incs)
        self._active_count = new_count
        LOG.debug("Old Count: %s, New Count: %s")

        if old_count == 0 and new_count > 0:
            await self._trigger_alarm()
        elif old_count > 0 and new_count == 0:
            await self._silence_alarm()


async def homepage(request):
    LOG.debug("howdy")
    return JSONResponse('Hello, world!')


async def startup():
    # NOTE: Under hypercorn, logging isn't configured until _after_ this
    global incidents
    incidents = IncidentTracker()
    LOG.info('Ready to go')


async def pdhook(request):
    global incidents
    event = await request.json()
    LOG.info("Event received: %r", event)
    
    if event['event']['data']['type'] == 'incident':
        task = BackgroundTask(incidents.update, event['event']['data'])
    else:
        task = None

    return JSONResponse({}, background=task)


routes = [
    Route('/', homepage),
    Route('/webhook/pagerduty/{ident}', pdhook, methods=['POST']),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
