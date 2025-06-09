from nicegui import ui, app

def darkmode_onchange(darkmode):
    if darkmode:
        ui.query('header').classes(add='to-black', remove='to-white')
        ui.query('footer div').classes(add='text-black', remove='text-white')
        ui.query('button').props(add='color=black', remove='color=white').style(add='color:black !important;', remove='color:white !important;')
    else:
        ui.query('header').classes(add='to-white', remove='to-black')
        ui.query('footer div').classes(add='text-white', remove='text-black')
        ui.query('button').props(add='color=white', remove='color=black').style(add='color:white !important;', remove='color:black !important;')

def main_color():
    if app.storage.user.get('darkmode',False): return "black"
    else:                                      return "white"

def darkmode_toggle():
    dark = ui.dark_mode(app.storage.user.get('darkmode',False), on_change=lambda e:darkmode_onchange(darkmode=e.value))
    darkmode_onchange(app.storage.user.get('darkmode',False))
    dark.bind_value(app.storage.user, 'darkmode')
    
    ui.switch('').props("checked-icon=light_mode unchecked-icon=dark_mode color=red-4 keep-color").bind_value(dark)