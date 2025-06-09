from nicegui import ui, Client
from lib.display_frog import frog_date
from lib.meta import balises


import datetime
import time

async def history(client):
    client.counter = 0
    today = datetime.date.today()
    ui.page_title(f'FOTD | history')
    balises("History", "/api/fotd", "/history")

    async def check():
        try:
            if await ui.run_javascript('window.pageYOffset >= document.body.offsetHeight - 2 * window.innerHeight'):
                date = ( today - datetime.timedelta(days=client.counter) ).strftime("%d-%m-%Y")
                with ui.column().classes("w-full md:w-5/12"):
                    frog_date(date).classes("w-full", remove="md:w-1/2")
                    ui.separator().classes('h-[2px]')
                client.counter += 1
        except TimeoutError:
            pass

    await client.connected()
    ui.timer(0.1, check)

        
