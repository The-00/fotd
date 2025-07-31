from nicegui import ui, app, Client
from fastapi import Request, Response, Query, Depends
from fastapi.responses import StreamingResponse
import os, io

import api.actions
import api.res.models

import pages.custom
import pages.experiment
import pages.fotd
import pages.history
import pages.playground

from lib.nav import header, footer
from lib.error import exception_handler_404, exception_handler_500
from lib.meta import balises


website=os.environ['WEBSITE']
favicon=f"{website}/res/logo.ico"

app.add_static_files('/res', 'res')

## APIs

def _stream_image(image, name):
    bio = io.BytesIO()
    image.save(bio, "PNG")
    bio.seek(0)
    return StreamingResponse(
            content=bio,
            media_type=f"image/png",
            headers={'Content-Disposition': f'filename="{name}"'}
        )

@app.get('/api/fotd', tags=["frog", "fotd"])
@app.get('/api/fotd/date/{date}', tags=["frog", "fotd"])
def get_frog_of_the_day(date=None, size:int=750) -> StreamingResponse:
    fotd = api.actions.api_fotd(date, size)
    image = fotd.get(size)
    return _stream_image(image, fotd.name)

@app.options('/api/fotd', tags=["frog", "fotd"])
@app.options('/api/fotd/date/{date}', tags=["frog", "fotd"])
def get_frog_of_the_day(date=None, size:int=750) -> StreamingResponse:
    fotd = api.actions.api_fotd(date, size)
    return fotd.data

@app.get('/api/frog/{seed:path}', tags=["frog"])
@app.get('/api/experiment/{mode}/{seed:path}', tags=["frog", "mushroom", "ghost"])
def get_image(seed:str="", characteristics:api.res.models.CharacterModel=Query(None), mode:api.actions.CharacterList=api.actions.CharacterList.frog, size:int=750) -> StreamingResponse:
    if not characteristics: characteristics=api.res.models.CharacterModel()
    character = api.actions.api_character(seed=seed, mode=mode, size=size, data=characteristics)
    image = character.get(size)
    return _stream_image(image, character.name)

@app.options('/api/frog/{seed:path}', tags=["frog"])
@app.options('/api/experiment/{mode}/{seed:path}', tags=["frog", "mushroom", "ghost"])
def get_image(seed:str="", characteristics:api.res.models.CharacterModel=Query(None), mode:api.actions.CharacterList=api.actions.CharacterList.frog, size:int=750) -> StreamingResponse:
    if not characteristics: characteristics=api.res.models.CharacterModel()
    character = api.actions.api_character(seed=seed, mode=mode, size=size, data=characteristics)
    return character.data

## Pages

@ui.page("/api")
async def api_doc():
    with header():
        ui.page_title(f'FOTD | API')
        ui.html("<iframe src='/api/docs' class='w-full h-full'></iframe>").classes("w-full h-full")
    footer()

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
        await pages.experiment.experiment(mode, seed)
    footer()

@ui.page("/playground")
async def experiment_frog(characteristics:api.res.models.CharacterModel=Query(None)):
    if not characteristics: characteristics=api.res.models.CharacterModel()
    with header():
        await pages.playground.playground(data=characteristics.model_dump())
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
