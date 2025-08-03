from nicegui import ui
from lib.display_frog import frog_date
from lib.meta import balises
import datetime

def date_or_today(date):
    today = datetime.date.today()
    if not date:
        return today
    elif type(date) == type(today):
        return today if date > today else date
    else:
        for f in ["%d-%m-%y", "%d-%m-%Y", "%d.%m.%y", "%d.%m.%Y", "%d/%m/%Y"]:
            try:
                date = datetime.datetime.strptime(date, f).date()
                break
            except ValueError:
                continue
        
        if type(date) == type(today):
            return today if date > today else date
        else:
            return today


def fotd(date=None):
    date = date_or_today(date).strftime("%d-%m-%Y")

    ui.page_title(f'FOTD | {date}')
    balises(date, f"/api/fotd/date/{date}", f"/{date}")
    frog_date(date)
