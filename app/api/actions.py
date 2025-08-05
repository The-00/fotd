from api.frog import Frog
from api.ghost import Ghost
from api.mushroom import Mushroom
from functools import lru_cache
from fastapi.responses import StreamingResponse
from api.res.models import CharacterModel, GhostModel, MushroomModel, FrogModel, DiffModel, AllCharacterModel
import munch

import datetime, time, io, re, os, enum

class CharacterList(enum.Enum):
    frog = "frog"
    mushroom = "mushroom"
    ghost = "ghost"

previous_day = None


def api_fotd(date=None, size:int=750):
    global previous_day
    used_date = None
    today = datetime.date.today()
    if not previous_day or previous_day < today:
        previous_day = today

    if date and type(date) == str:
        for f in ["%d-%m-%y", "%d-%m-%Y", "%d.%m.%y", "%d.%m.%Y", "%d/%m/%Y"]:
            try:
                date = datetime.date.fromtimestamp( datetime.datetime.strptime(date, f).timestamp() )
                if date <= today:
                    used_date = date
                    break
            except:
                continue

        if not used_date:
            used_date = today

    else:
        used_date = today

    fotd_seed = used_date.strftime( os.environ['FOTD_FORMAT'] if 'FOTD_FORMAT' in os.environ else "%d-%m-%Y(%w|%j)")
    fotd_name = used_date.strftime("%d-%m-%Y")
    
    return get_character(size=size, seed=fotd_seed, name=fotd_name)


def api_character(size:int=750, seed="random", mode:CharacterList=CharacterList.frog, data:CharacterModel=CharacterModel()):
    return get_character(size=size, seed=seed, name=f"{mode.value} - {seed}", mode=mode, data=data)

def api_url(size:int=750, seed="random", mode:CharacterList=CharacterList.frog, data:CharacterModel=CharacterModel()):
    character_seeded = get_character(size=size, seed=seed, name=f"{mode.value} - {seed}", mode=mode)
    character_dataed = get_character(size=size, seed=seed, name=f"{mode.value} - {seed}", mode=mode, data=data)
    
    character_diff = DiffModel.diff(character_seeded.data, character_dataed.data)

    return munch.Munch({"seed": seed, "data":character_diff.model_dump_json(exclude_unset=True), "mode": mode.value})

@lru_cache()
def get_character(size:int, seed:str, name:str=None, mode:CharacterList=CharacterList.frog, data:CharacterModel=CharacterModel()):
    if mode:
        if mode == CharacterList.ghost:
            return Ghost(size=size, seed=seed, name=name, data=GhostModel(**data.model_dump()))
        elif mode == CharacterList.mushroom:
            return Mushroom(size=size, seed=seed, name=name, data=MushroomModel(**data.model_dump()))
        elif mode == CharacterList.frog:
            return Frog(size=size, seed=seed, name=name, data=FrogModel(**data.model_dump()))
    else:
        return Frog(size=size, seed=seed, name=name, data=FrogModel(**data.model_dump()))
