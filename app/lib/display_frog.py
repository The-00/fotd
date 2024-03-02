from nicegui import ui
import requests
import urllib.parse
import os

def _download(url, name):
    ui.download(src=url, filename=name)

def _clip_url(url):
    full_url = os.environ['WEBSITE'] 
    if url.startswith("/api/fotd/date/"):
        full_url += '/'+ "/".join( url.split("/")[4:] )
    elif url.startswith("/api/frog/"):
        full_url += '/custom/'+ "/".join( url.split("/")[3:] )
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
        with ui.row().classes("w-full max-h-full h-full relative"):
            ui.image(url).props(f"fit=contain content='{alt} | {txt}'").classes("w-full max-h-full")
            with ui.row().classes("w-full absolute bottom-px gap-0"):
                ui.label(txt).classes("text-center font-mono text-red-400 text-2xl w-full")
                with ui.row().classes("w-full text-center justify-center"):
                    ui.button(icon="download", on_click=lambda e:_download(url, f"{alt}_{txt}.png")) \
                        .classes("bg-white text-center").props("round flat color=red-400 ") \
                        .tooltip("Download Image")
                    ui.button(icon="content_copy", on_click=lambda e:_clip_url(url)) \
                        .classes("bg-white text-center").props("round flat color=red-400 ") \
                        .tooltip("Copy URL")
                    ui.button(icon="perm_media", on_click=lambda e:_clip_image(url)) \
                        .classes("bg-white text-center").props("round flat color=red-400 ") \
                        .tooltip("Copy Image")

    return frog_bundle

def frog_date(date):
    date_safe = urllib.parse.quote( date )
    url = f'/api/fotd/date/{date_safe}'
    alt = 'Frog Of The Day'
    txt = date

    return _frog(txt, url, alt)

def frog_seed(seed:str=""):
    seed_safe = urllib.parse.quote( seed , safe='')
    url = f'/api/frog/{seed_safe}'
    alt = 'Custom Frog'
    txt = seed if seed and seed != "" else "Random"

    return _frog(txt, url, alt)