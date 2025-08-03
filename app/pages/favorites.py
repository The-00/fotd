from nicegui import ui, Client, app
from lib.display_frog import _frog, frog_seed
from lib.meta import balises


import datetime
import time

async def favorites():
    ui.page_title(f'FOTD | favorites')
    balises("Favorites", "/api/fotd", "/favorites")

    for el in app.storage.user.get("fav", {}):
        with ui.column().classes("w-full md:w-1/3"):
            _frog(el, app.storage.user["fav"][el], el).classes("w-full", remove="md:w-1/2")
            ui.separator().classes('h-[2px]')
    
    if len(app.storage.user.get("fav", {}).keys()) == 0:
        with ui.column().classes("w-full md:w-1/3"):
            frog_seed("Nothing to see here").classes("w-full", remove="md:w-1/2")
            ui.separator().classes('h-[2px]')

        
