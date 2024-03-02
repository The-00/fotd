from api.frog import Frog
from functools import lru_cache
from fastapi.responses import StreamingResponse

import datetime, time, io, re, os

previous_day = None

def return_frog_img(frog, size=None):
    img = frog.get(size if size else frog.size)
    bio = io.BytesIO()

    img.save(bio, "PNG")
    bio.seek(0)

    return StreamingResponse(
            content=bio,
            media_type=f"image/png",
            headers={'Content-Disposition': f'filename="{frog.name}"'}
        )

def api_fotd(days=0, date=None, size=None):
    fotd = get_fotd(days, date, size)
    
    return return_frog_img(fotd)


def api_seed_frog(seed=None, size:int=750):
    name = None

    if not seed or seed=="random":
        return return_frog_img(get_frog(size=size, seed=seed, name="random"))

    frog = get_frog_cached(seed=seed, size=size, name=name)
    
    return return_frog_img(frog)

@lru_cache()
def get_fotd(days=0, date=None, size=1000):
    global previous_day
    used_date = None
    today = datetime.date.today()
    if not previous_day or previous_day < today:
        previous_day = today

    if date and type(date) == str:
        for f in ["%d-%m-%y", "%d-%m-%Y", "%d.%m.%y", "%d.%m.%Y"]:
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
        days = abs(days)
        used_date = today - datetime.timedelta(days=days)

    fotd_seed = used_date.strftime( os.environ['FOTD_FORMAT'] if 'FOTD_FORMAT' in os.environ else "%d-%m-%Y(%w|%j)")
    fotd_name = used_date.strftime("%d-%m-%Y")
    
    fotd_obj = get_frog(size, fotd_seed, fotd_name)
    return fotd_obj

def get_frog(size, seed, name=None):
    frog = Frog(size=size, seed=seed, name=name)

    return frog

@lru_cache()
def get_frog_cached(size, seed, name=None):
    return get_frog(size=size, seed=seed, name=name)
