from nicegui import ui


def header():
    with ui.header(elevated=False, wrap=False).classes('items-center justify-between bg-transparent flex'):

        with ui.row().classes("flex"):
            with ui.link("", "/").classes("no-underline contents"):
                ui.image('/res/logo.svg').classes('max-w-12 w-12 fill-red-400')
                ui.label('Frog Of The Day').classes("text-red-400 text-2xl font-mono self-center")

        with ui.button(icon='menu').props('flat color=white').classes('bg-red-400 w-full sm:w-fit'):
            with ui.menu().classes("w-1/2 sm:w-1/6") as menu:
                with ui.menu_item(None, lambda:ui.navigate.to("/")):
                    ui.button("Today", icon="today").props('flat color=white').classes('bg-red-400 w-full font-mono')
                with ui.menu_item(None, lambda:ui.navigate.to("/custom")):
                    ui.button("Custom", icon="tune").props('flat color=white').classes('bg-red-400 w-full font-mono')
                with ui.menu_item(None, lambda:ui.navigate.to("/history")):
                    ui.button("History", icon="history").props('flat color=white').classes('bg-red-400 w-full font-mono')
                with ui.menu_item(None, lambda:ui.navigate.to("/api")):
                    ui.button("API", icon="api").props('flat color=white').classes('bg-red-400 w-full font-mono')
                    
    content = ui.row().classes('flex w-full justify-center m-0 overflow-hidden').style("height:75vh;")
    return content
    

def footer():
    with ui.footer().classes('justify-between bg-red-400 py-px'):
        ui.markdown('Made by *Unicolore*').classes('text-white font-mono')
        with ui.link("", "https://nicegui.io/").classes("no-underline font-mono"):
            ui.markdown("Powered by **NiceGUI**").classes('text-white')
