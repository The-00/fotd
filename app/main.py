from nicegui import ui, app, Client
from fastapi import Request, Response, Query, Depends
from fastapi.responses import StreamingResponse
from fastapi.exceptions import RequestValidationError
from pydantic import Json
import os, io

import api.actions
import api.res.models

import pages.custom
import pages.fotd
import pages.history
import pages.favorites
import pages.playground

from lib.nav import header, footer
from lib.error import exception_handler_404, exception_handler_422, exception_handler_500
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

@app.get('/api/fotd/{date:path}', tags=["fotd"])
def get_frog_of_the_day(date=None, size:int=750) -> StreamingResponse:
    fotd = api.actions.api_fotd(date, size)
    image = fotd.get(size)
    return _stream_image(image, fotd.name)

@app.options('/api/fotd/{date:path}', tags=["fotd"])
def get_frog_of_the_day_data(date=None, size:int=750) -> StreamingResponse:
    fotd = api.actions.api_fotd(date, size)
    return fotd.data

@app.get('/api/{mode}/{seed:path}', tags=["character"])
def get_image(seed:str="", data:Json=Query(None), mode:api.actions.CharacterList=api.actions.CharacterList.frog, size:int=750) -> StreamingResponse:
    if not data: data=api.res.models.CharacterModel()
    if mode == api.actions.CharacterList.frog:     data = api.res.models.FrogModel(**data)
    if mode == api.actions.CharacterList.ghost:    data = api.res.models.GhostModel(**data)
    if mode == api.actions.CharacterList.mushroom: data = api.res.models.MushroomModel(**data)

    character = api.actions.api_character(seed=seed, mode=mode, size=size, data=data)
    image = character.get(size)
    return _stream_image(image, character.name)

@app.options('/api/{mode}/{seed:path}', tags=["character"])
def get_data(seed:str="", data:Json=Query(None), mode:api.actions.CharacterList=api.actions.CharacterList.frog, size:int=750) -> StreamingResponse:
    if not data: data=api.res.models.CharacterModel()
    if mode == api.actions.CharacterList.frog:     data = api.res.models.FrogModel(**data)
    if mode == api.actions.CharacterList.ghost:    data = api.res.models.GhostModel(**data)
    if mode == api.actions.CharacterList.mushroom: data = api.res.models.MushroomModel(**data)
    
    character = api.actions.api_character(seed=seed, mode=mode, size=size, data=data)
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

@ui.page("/favorites")
async def favorites():
    with header() as favorites_header:
        favorites_header.classes(remove="overflow-hidden").style(remove="height:72vh;")
        await pages.favorites.favorites()
    footer()

@ui.page("/custom")
@ui.page("/custom/{mode}")
@ui.page("/custom/{mode}/{seed:path}")
async def get_image(seed:str="", data:Json=Query(None), mode:api.actions.CharacterList=api.actions.CharacterList.frog, size:int=750):
    if not data: data=api.res.models.CharacterModel()
    if mode == api.actions.CharacterList.frog:     data = api.res.models.FrogModel(**data)
    if mode == api.actions.CharacterList.ghost:    data = api.res.models.GhostModel(**data)
    if mode == api.actions.CharacterList.mushroom: data = api.res.models.MushroomModel(**data)
    with header():
        await pages.custom.custom(mode=mode, seed=seed, data=data)
    footer()

@app.exception_handler(404)
async def app_exception_handler_404(request: Request, exception: Exception) -> Response:
    return exception_handler_404(request, exception)

@app.exception_handler(RequestValidationError)
async def app_exception_handler_422(request: Request, exception: Exception) -> Response:
    return exception_handler_422(request, exception)

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
