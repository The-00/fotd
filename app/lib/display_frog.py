from nicegui import ui, app
from lib.darkmode import main_color
import requests
import urllib.parse
import os
import json

from api.actions import api_character, api_url, CharacterList

def _fav(url, name, element):
    if "fav" not in  app.storage.user: app.storage.user['fav'] = {}

    if name in app.storage.user['fav']:
        del(app.storage.user['fav'][name])
        element.props(add='color=red-400', remove='color=yellow-400')
    else:
        app.storage.user['fav'][name] = url
        element.props(add='color=yellow-400', remove='color=red-400')
    
def _download(url, name):
    ui.download(src=url, filename=name)

def _clip_url(url):
    full_url = os.environ['WEBSITE']
    url_type = url.split("/")[2]
    if url_type == "fotd":
        full_url += '/'+ "/".join( url.split("/")[3:] )
    elif url_type in [e.value for e in CharacterList]:
        full_url += '/custom/'+ "/".join( url.split("/")[2:] )
    else:
        full_url += "/"
    ui.run_javascript(f'navigator.clipboard.writeText("{full_url}")')
    ui.notify("URL copied to clipboard")

def _clip_image(url):
    full_url = os.environ['WEBSITE'] + url.replace("'", "\'")
    ui.run_javascript('''
const setToClipboard = async blob => {
  const data = [new ClipboardItem({ [blob.type]: blob })]
  await navigator.clipboard.write(data)
}''' +f'''
  const response = await fetch('{url}')
  const blob = await response.blob()
  await setToClipboard(blob) 
    ''')
    ui.notify("Image copied to clipboard")

def _frog(txt, url, alt):
    with ui.row().classes("w-full justify-center h-full md:w-1/2 ") as frog_bundle:
        with ui.column().classes("w-full max-h-full h-full relative"):
            ui.image(url).props(f"fit=contain content='{alt} | {txt}'").classes("w-full max-h-full")
            with ui.column().classes("w-full relative bottom-px gap-0"):
                ui.label(txt).classes("text-center font-mono text-red-400 text-2xl w-full")
                with ui.row().classes("w-full text-center justify-center"):
                    ui.button(icon="download", on_click=lambda e:_download(url, f"{alt}_{txt}.png")) \
                        .classes(f"bg-transparent text-center").props("round flat color=red-400 ") \
                        .tooltip("Download Image")
                    ui.button(icon="content_copy", on_click=lambda e:_clip_url(url)) \
                        .classes(f"bg-transparent text-center").props("round flat color=red-400 ") \
                        .tooltip("Copy URL")
                    ui.button(icon="perm_media", on_click=lambda e:_clip_image(url)) \
                        .classes(f"bg-transparent text-center").props("round flat color=red-400 ") \
                        .tooltip("Copy Image")
                    ui.button(icon="star", on_click=lambda e:_fav(url, txt, e.sender)) \
                        .classes(f"bg-transparent text-center").props(f"round flat color={'red-400' if txt not in app.storage.user.get('fav',{}) else 'yellow-400'} ") \
                        .tooltip("Favorite")

    return frog_bundle

def frog_date(date):
    date_safe = urllib.parse.quote( date )
    url = f'/api/fotd/{date_safe}'
    alt = 'Frog Of The Day'
    txt = date

    return _frog(txt, url, alt)

def frog_seed(seed:str="", mode=None):
    seed_safe = urllib.parse.quote( seed , safe='')
    url = f'/api/frog/{seed_safe}'  if not mode else f'/api/experiment/{mode}/{seed_safe}'
    alt = 'Custom Frog' if not mode else f'Experiment {mode}'
    txt = seed if seed and seed != "" else "Random"

    return _frog(txt, url, alt)

def frog_data(data:dict={}):
    data_safe = urllib.parse.quote( json.dumps(data) , safe='')
    url = f'/api/frog/?characteristics={data_safe}'
    alt = 'Playground Frog'
    txt = 'Playground'

    return _frog(txt, url, alt)

def character_element(mode, seed, data):
    url_data = api_url(seed=seed, mode=mode, data=data)

    url = f"/api/{urllib.parse.quote( url_data.mode , safe='')}/{urllib.parse.quote( url_data.seed , safe='')}"
    txt = f"{url_data.mode.capitalize()} {url_data.seed}"
    alt = f"{url_data.mode.capitalize()} {url_data.seed}"
    
    if url_data.data != "{}":
        data_safe = urllib.parse.quote( url_data.data , safe='')
        url += f"?data={data_safe}"
        alt += " (customized)"
        txt += "*"

    return _frog(txt, url, alt)