from nicegui import ui, app, Client
from fastapi import Request, Response
import os

import api.actions

import pages.custom
import pages.experiment
import pages.fotd
import pages.history

from lib.nav import header, footer
from lib.error import exception_handler_404, exception_handler_500
from lib.meta import balises


website=os.environ['WEBSITE']
favicon=f"{website}/res/logo.ico"

app.add_static_files('/res', 'res')

@ui.page("/api")
async def api_doc():
    with header():
        ui.page_title(f'FOTD | API')
        ui.html("<iframe src='/api/docs' class='w-full h-full'></iframe>").classes("w-full h-full")
    footer()

@app.get('/api/fotd')
@app.get('/api/fotd/days/{days}')
@app.get('/api/fotd/date/{date}')
def fotd(days:int=0, date=None, size:int=750):
    return api.actions.api_fotd(days, date, size)

@app.get('/api/frog/{seed:path}')
@app.get('/api/frog')
def seed_frog(seed=None, size:int=750):
    return api.actions.api_seed_frog(seed, size)

@app.get('/api/experiment/{mode}')
@app.get('/api/experiment/{mode}/{seed:path}')
def seed_frog(mode:str, seed=None, size:int=750):
    return api.actions.api_seed_frog(seed, size, mode=mode)

@ui.page("/history")
async def history(client:Client):
    with header() as history_header:
        history_header.classes(remove="overflow-hidden").style(remove="height:72vh;")
        await pages.history.history(client)
    footer()

@ui.page("/custom")
@ui.page("/custom/{seed:path}")
async def custom_frog(seed=""):
    with header():
        await pages.custom.custom_frog(seed)
    footer()

@ui.page("/experiment")
@ui.page("/experiment/{mode}")
@ui.page("/experiment/{mode}/{seed:path}")
async def experiment_frog(mode="ghost", seed=""):
    with header():
        await pages.experiment.experiment_frog(mode, seed)
    footer()

@app.exception_handler(404)
async def app_exception_handler_404(request: Request, exception: Exception) -> Response:
    return exception_handler_404(request, exception)

@app.exception_handler(500)
async def app_exception_handler_500(request: Request, exception: Exception) -> Response:
    return exception_handler_500(request, exception)

@ui.page('/')
@ui.page('/{date}')
async def main(date:str=None):
    with header():
        pages.fotd.fotd(date)
    footer()

app.docs_url = "/api/docs"
app.openapi_url = "/api/openapi.json"
app.redoc_url = "/api/redoc"
ui.run(favicon=favicon, show=False, title="FOTD", storage_secret=os.environ['STORAGE_SECRET'], uvicorn_logging_level='info', fastapi_docs=True)
