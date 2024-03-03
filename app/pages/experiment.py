from nicegui import ui, run
from debouncer import DebounceOptions, debounce
from lib.display_frog import frog_seed
from lib.meta import balises
import random
import names

async def generate_random(seed_input, frog_image, mode):
    seed = "".join([random.choice("abcdefghijklmnopqrstuvwxyz1234567890-") for _ in range(25)])
    seed = names.get_full_name()

    seed_input.set_value(seed)
    await change_image(seed, frog_image, mode)



@debounce(wait=.5, options=DebounceOptions(trailing=True, leading=False, time_window=3))
async def change_image(seed, element, mode):
    element.clear()

    with element:
        ui.page_title(f'FOTD | {mode} | {seed}')
        seed_safe = seed.replace("'", "\\'")
        mode_safe = mode.replace("'", "\\'")
        ui.run_javascript(f'''
        const seed = '{seed_safe}';
        const mode = '{mode_safe}';
        const nextURL = '/experiment/' + mode + '/' + seed;
        const nextTitle = 'FOTD | '+mode+' |' + seed;''' +
        '''
        const nextState = { additionalInformation: 'Updated the URL with JS' };
        // window.history.pushState(nextState, nextTitle, nextURL);
        window.history.replaceState(nextState, nextTitle, nextURL);
        ''')
        frog_seed(seed, mode).classes(remove="md:w-1/2")

async def experiment_frog(mode, seed:str=""):
    with ui.row().classes('flex w-full h-4/5 md:h-full justify-center flex-row-reverse'):
        with ui.row().classes("sm:w-4/5 md:w-1/2 w-full max-h-full h-full justify-center") as frog_image:
            frog_seed(seed, mode).classes(remove="md:w-1/2")

        with ui.row().classes("m-auto text-3xl w-full sm:w-3/5 md:w-1/3 place-content-around"):
            ui.button(icon='shuffle',
                    on_click=lambda e: generate_random( seed_input, frog_image, mode )
                ).classes("bg-white text-center self-center").props("round flat color=red-400 ")
            
            seed_input = ui.input(label='Frog Name', value=seed) \
                .classes('m-auto text-3xl w-4/5 text-red-400') \
                .on("update:model-value",handler=lambda e: change_image(e.args, frog_image, mode)).props("filled color=red-400 label-color=red-400 input-style='color: rgb(248 113 113);'")
            
            ui.toggle(options=["ghost","frog"], on_change=lambda e:ui.navigate.to(f"/experiment/{e.value}/{seed_input.value}"), value=mode) \
                .classes('m-auto text-3xl text-red-400') \
                .props("filled toggle-text-color=white toggle-color=red-400")


    if seed == "":
        await generate_random(seed_input, frog_image, mode)
        balises(f"{mode}", f'/api/experiment/{mode}', f'/experiment/{mode}')
    else:
        ui.page_title(f'FOTD | {mode} | {seed}')
        balises(f"{mode} | {seed}", f'/api/experiment/{mode}/{seed}', f'/experiment/{mode}/{seed}')


