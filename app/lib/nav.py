from nicegui import ui
from lib.darkmode import darkmode_toggle, main_color


def header():
    with ui.header(elevated=False, wrap=False).classes(f'items-center justify-between bg-gradient-to-t from-transparent to-{main_color()} flex').style('background-color:transparent;') as navheader:

        with ui.row().classes("flex"):
            with ui.link("", "/").classes("no-underline contents"):
                ui.image('/res/logo.svg').classes('max-w-12 w-12 fill-red-400')
                ui.label('Frog Of The Day').classes("text-red-400 text-2xl font-mono self-center")

        with ui.row().classes("flex w-full sm:w-fit"):
            with ui.row().classes("size-2/12 sm:w-fit"):
                darkmode_toggle()
            with ui.button(icon='menu').props(f'flat color={main_color()}').classes('bg-red-400 size-9/12 sm:w-fit'):
                with ui.menu().classes("w-1/2 sm:w-1/6") as menu:
                    with ui.menu_item(None, lambda:ui.navigate.to("/")):
                        ui.button("Today", icon="today").props(f'flat color={main_color()}').classes('bg-red-400 w-full font-mono')
                    with ui.menu_item(None, lambda:ui.navigate.to("/history")):
                        ui.button("History", icon="history").props(f'flat color={main_color()}').classes('bg-red-400 w-full font-mono')
                    with ui.menu_item(None, lambda:ui.navigate.to("/custom")):
                        ui.button("Custom", icon="tune").props(f'flat color={main_color()}').classes('bg-red-400 w-full font-mono')
                    with ui.menu_item(None, lambda:ui.navigate.to("/favorites")):
                        ui.button("Favorites", icon="star").props(f'flat color={main_color()}').classes('bg-red-400 w-full font-mono')
                    with ui.menu_item(None, lambda:ui.navigate.to("/api")):
                        ui.button("API", icon="api").props(f'flat color={main_color()}').classes('bg-red-400 w-full font-mono')
                    
    content = ui.row().classes('flex w-full justify-center m-0 overflow-hidden').style("height:72vh;")
    return content
    

def footer():
    with ui.footer().classes('justify-between bg-red-400 py-px text-xs'):
        with ui.link("", "https://github.com/The-00/fotd/", new_tab=True).classes("no-underline font-mono"):
            ui.markdown('Made by *Unicolore*').classes(f'text-{main_color()} font-mono')
        with ui.link("", "https://nicegui.io/", new_tab=True).classes("no-underline font-mono"):
            ui.markdown("Powered by **NiceGUI**").classes(f'text-{main_color()}')
