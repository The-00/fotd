from frog import Frog
from bottle import Bottle, get, response, HTTPError
import datetime
import io
import json
import base64

app = Bottle()

template = ""
with open("/fotd/template.html") as templatefile:
    for l in templatefile:
        template += l

def generate(size, seed=None, data={}):
    frog = Frog(size=size, seed=seed, data=data)
    return frog.get(size)

@app.get("/api/<seed>/")
@app.get("/api/<seed>")
@app.get("/api/")
@app.get("/api")
def get_frog( seed=None ):

    frog_img = generate(size=700, seed=seed)

    if response:
        response.set_header('Content-type', 'image/png')
        response.set_header('Content-disposition', f'filename="random{"-with-seed-" + seed if seed else ""}.png"')

    membuf = io.BytesIO()
    frog_img.save(membuf, format="png")

    return membuf.getvalue()

@app.get("/custom/<b64>/")
@app.get("/custom/<b64>")
def custom(b64=None):
    try:
        json_string = base64.b64decode(b64)
        data = json.loads( json_string )

        frog_img = generate(size=700, data=data)

        if response:
            response.set_header('Content-type', 'image/png')
            response.set_header('Content-disposition', 'filename="custom.png"')

        membuf = io.BytesIO()
        frog_img.save(membuf, format="png")

        return membuf.getvalue()
    except Exception as e:
        raise HTTPError(500, f"got error {e}")


@app.get("/fotd/")
@app.get("/fotd")
def get_fotd():

    today = datetime.date.today().strftime("%d-%m-%Y")
    frog_img = generate(size=600, seed=today)

    if response:
        response.set_header('Content-type', 'image/png')
        response.set_header('Content-disposition', 'filename="fotd.png"')

    membuf = io.BytesIO()
    frog_img.save(membuf, format="png")

    return membuf.getvalue()

@app.get("/")
def disp_fotd():
    base64_img = base64.b64encode( get_fotd() ).decode('ascii')
    if response:
        response.set_header('Content-type', 'text/html')
    content = '''
			<div class="center space">
				<img src="data:image/png;base64,''' + base64_img + '''" class="logo" />
			</div>
			<div class="space center ">
				<h1 class="title">Frog Of The Day</h1>
			</div>
'''
    return template.replace("{{CONTENT}}", content)


@app.get("/help/")
@app.get("/help")
def help():
    content = """<div class="space center">
                <h1 class="title">How To Use FOTD</h1>
                <table>
                    <tr>
                        <th>Endpoint</th>
                        <th>Usage</th>
                    </tr>
                    <tr>
                        <td>/</td>
                        <td>The fotd in a beautiful format</td>
                    </tr>
                    <tr>
                        <td>/fotd</td>
                        <td>The fotd in a usable format</td>
                    </tr>
                    <tr>
                        <td>/api</td>
                        <td>A random frog in a usable format</td>
                    </tr>
                    <tr>
                        <td>/api/[SEED]</td>
                        <td>A random frog generated with the SEED in a usable format</td>
                    </tr>
                    <tr>
                        <td>/help</td>
                        <td>This help page</td>
                    </tr>
                </table>
                </div>
"""
    return template.replace("{{CONTENT}}", content)


app.run(host="0.0.0.0", port=8080, server='paste', reloader=True)
