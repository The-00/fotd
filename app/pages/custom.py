from nicegui import ui, run
from debouncer import DebounceOptions, debounce
from lib.display_frog import character_element
from lib.darkmode import main_color
from lib.meta import balises
import random
import names
import json
import urllib.parse

# on profite que l'app soit monolitique
from api.res.models import CharacterModel
from api.actions import api_character, CharacterList, api_url

async def generate_random(seed_input, data_input, character_image, mode_input):
    # seed = "".join([random.choice("abcdefghijklmnopqrstuvwxyz1234567890-") for _ in range(25)])
    seed = names.get_full_name()

    seed_input.set_value(seed)
    await change_image(mode_input, seed_input, data_input, character_image)

async def update_browser(mode, seed, data="{}"):
    title = f'FOTD | {mode.value} | {seed}'
    url   = f"{urllib.parse.quote( mode.value , safe='')}/{urllib.parse.quote( seed , safe='')}"
    if data != "{}":
        title += '*'
        url   += f"?data={urllib.parse.quote( data, safe='')}"
    
    ui.page_title(title)
    ui.navigate.history.push('/custom/' + url)
    balises(title, '/api' + url, '/custom' + url)

@debounce(wait=.5, options=DebounceOptions(trailing=True, leading=False, time_window=3))
async def change_image(mode_input, seed_input, data_input, element, reset=True):
    mode = CharacterList(mode_input.value)
    seed = seed_input.value
    data = (await data_input.run_editor_method("get"))["json"]
    element.clear()

    if reset:
        data = {}

    with element:
        character_element(mode, seed, CharacterModel(**data)).classes(remove="md:w-1/2")
        character_json = json.loads(api_character(seed=seed, mode=mode, data=CharacterModel(**data)).data.model_dump_json())
        url_data = api_url(seed=seed, mode=mode, data=CharacterModel(**data))
        data_input.run_editor_method("update", {'json': character_json})
        await update_browser(mode, seed, url_data.data)

async def custom(mode:CharacterList,  data:CharacterModel, seed:str=""):
    with ui.row().classes('flex w-full h-4/5 md:h-full justify-center flex-row-reverse'):
        character_image = ui.row().classes("sm:w-4/5 md:w-1/2 w-full max-h-full h-full justify-center")

        with ui.row().classes("m-auto text-3xl w-full sm:w-3/5 md:w-1/3 place-content-around"):
            ui.button(icon='shuffle',
                    on_click=lambda e: generate_random( seed_input, data_input, character_image, mode_input )
                ).classes(f"text-center self-center bg-transparent").props("round flat color=red-400 ")
            
            seed_input = ui.input(label='Character Name', value=seed) \
                .classes('m-auto text-3xl w-4/5 text-red-400') \
                .on("update:model-value",handler=lambda e: change_image(mode_input, seed_input, data_input, character_image)).props("filled color=red-400 label-color=red-400 input-style='color: rgb(248 113 113);'")
            
            mode_input = ui.toggle(options=list(CharacterList), on_change=lambda e: change_image(mode_input, seed_input, data_input, character_image, False), value=mode) \
                .classes('m-auto text-3xl text-red-400') \
                .props(f"filled toggle-text-color={main_color()} toggle-color=red-400")

            with ui.expansion('Advanced').classes('w-full m-auto text-3xl w-4/5 text-red-400 text-center h-4/5'):
                schema = CharacterModel.model_json_schema(by_alias=True)
                data_input = ui.json_editor({'content': {'json': json.loads(data.model_dump_json())}},
                    on_change=lambda e: change_image(mode_input, seed_input, data_input, character_image, reset=False),
                    schema=schema)\
                    .classes('m-auto text-3xl w-4/5 text-red-400 max-h-full h-full')


    title = f'FOTD | {mode.value}'
    url   = f"{urllib.parse.quote( mode.value , safe='')}"
    if seed != "":
        title += f" | {seed}"
        url   += f"/{urllib.parse.quote( seed , safe='')}"
        if data.model_dump_json() != "{}":
            url += f"?data={urllib.parse.quote( data.model_dump_json(), safe='')}"
        await change_image(mode_input, seed_input, data_input, character_image, False)
    else:
        await generate_random(seed_input, data_input, character_image, mode_input)
    balises(title, '/api/' + url, '/custom/' + url)



