from nicegui import ui, run
from debouncer import DebounceOptions, debounce
from lib.display_frog import frog_data
from lib.darkmode import main_color
from lib.meta import balises
import random
import names
import json

# on profite que l'app soit monolitique
from api.res.models import CharacterModel
from api.actions import api_character, CharacterList



@debounce(wait=.5, options=DebounceOptions(trailing=True, leading=False, time_window=3))
async def change_image(data, element):
    element.clear()

    with element:
        frog_data(data).classes(remove="md:w-1/2")

async def playground(data:dict={}, mode="frog"):
    data = json.loads(api_character(data=CharacterModel(**data)).data.model_dump_json())

    with ui.row().classes('flex w-full h-4/5 md:h-full justify-center flex-row-reverse'):
        with ui.row().classes("sm:w-4/5 md:w-1/2 w-full max-h-full h-full justify-center") as frog_image:
            frog_data(data).classes(remove="md:w-1/2")

        with ui.row().classes("m-auto text-3xl w-full sm:w-3/5 md:w-1/3 max-h-full h-full place-content-around"):

            schema = CharacterModel.model_json_schema(by_alias=True)

            data_input = ui.json_editor({'content': {'json': data}},
                on_change=lambda e: change_image(e.content["json"], frog_image),
                schema=schema)\
                .classes('m-auto text-3xl w-4/5 text-red-400 max-h-full h-4/5')
            
            # mode_input = ui.toggle(options=list(CharacterList), value=CharacterList.frog) \
            #     .classes('m-auto text-3xl text-red-400') \
            #     .props(f"filled toggle-text-color={main_color()} toggle-color=red-400")