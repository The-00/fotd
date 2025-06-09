from nicegui import ui, Client
from fastapi import Request, Response

from lib.nav import header, footer
from lib.display_frog import frog_seed

def exception_handler_404(request: Request, exception: Exception) -> Response:
    with Client(ui.page(''), request=request) as client:
        error(404, "Page not found")
    return client.build_response(request, 404)

def exception_handler_500(request: Request, exception: Exception) -> Response:
    with Client(ui.page(''), request=request) as client:
        error(500, "Something went wrong")
        
    return client.build_response(request, 500)


def error(v, info):
    with header():
        with ui.row().classes("m-auto text-3xl w-full sm:w-3/5 md:w-1/3 place-content-around"):
            with ui.column().classes('m-auto'):
                ui.label(f'Error {v}').classes("text-red-400 text-6xl font-mono self-center")
                ui.label(info).classes("text-red-400 text-3xl font-mono self-center")
        with ui.row().classes("sm:w-4/5 md:w-1/2 w-full max-h-full h-full justify-center"):
            frog_seed(str(v)).classes(remove="md:w-1/2")
    footer()