from frog import Frog
from bottle import Bottle, get, response
import datetime
import io
import base64

frogsize = 400

app = Bottle()

def generate(size, seed):
    frog = Frog(size=size, seed=seed)
    return frog.get(size)

@app.get("/api/<seed>/")
@app.get("/api/<seed>")
@app.get("/api/")
@app.get("/api")
def get_frog( seed=None ):

    frog_img = generate(size=700, seed=seed)

    if response:
        response.set_header('Content-type', 'image/png')
        response.set_header('Content-disposition', 'filename="braaah.png"')

    membuf = io.BytesIO()
    frog_img.save(membuf, format="png")

    return membuf.getvalue()

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
    return '''<html>
	<head>
		<meta charset="UTF-8">
		<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Ubuntu" />
		<style type="text/css">
			body{
				font-family: Ubuntu;
				font-size: 14px;
				font-style: normal;
				font-variant: normal;
				font-weight: 400;
				line-height: 20px;
			}
			.center{
				text-align: center;
			}
			.title{
				text-transform: uppercase;
			}
			.logo {
				display: block;
				margin: auto;
				max-width: 50vw;
			}
			.space{
				padding-x: 25px;
			}
		</style>
	</head>
	<body>
		<div>
			<div class="center space">
				<img src="data:image/png;base64,''' + base64_img + '''" class="logo" />
			</div>
			<div class="space center ">
				<h1 class="title">Frog Of The Day</h1>
			</div>
		</div>
	</body>
</html>
'''

@app.get("/help/")
@app.get("/help")
def help():
    return '''<html>
	<head>
		<meta charset="UTF-8">
		<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Ubuntu" />
		<style type="text/css">
			body{
				font-family: Ubuntu;
				font-size: 14px;
				font-style: normal;
				font-variant: normal;
				font-weight: 400;
				line-height: 20px;
			}
			.center{
				text-align: center;
			}
			.title{
				text-transform: uppercase;
			}
			.logo {
				display: block;
				margin: auto;
				max-width: 50vw;
			}
			.space{
				padding-x: 25px;
			}
            table, th, td {
                border:1px solid black;
                border-collapse: collapse;
            }
            table {
				margin: auto;
				max-width: 50vw;
            }
		</style>
	</head>
	<body>
		<div>
			<div class="space center ">
	    		<h1 class="title">How To Use FOTD</h1>
                <table style="border:solid">
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
		</div>
	</body>
</html>
'''


app.run(host="0.0.0.0", port=8080, server='paste', reloader=True)
