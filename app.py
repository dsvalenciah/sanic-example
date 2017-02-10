#bultin library

#external libraries
from sanic import Sanic
from sanic.response import json, html
from jinja2 import Environment, PackageLoader
from CRUD import *

env = Environment(
    loader=PackageLoader('app', 'templates'),
)

app = Sanic(__name__)

app.static('/static', './static')

@app.route("/")
async def home(request):
    template = env.get_template("home.html")
    html_content = template.render()
    return html(html_content)

@app.route("/sign_up")
async def sign_up(request):
    template = env.get_template("sign_up.html")
    html_content = template.render()
    return html(html_content)

@app.route("/save_user", methods=["POST"])
async def save_user(request):
    add_user(
        name=request.form["user"][0],
        password=request.form["password"][0],
    )
    template = env.get_template("home.html")
    html_content = template.render()
    return html(html_content)

@app.route("/login")
async def login(request):
    template = env.get_template("login.html")
    html_content = template.render()
    return html(html_content)

@app.route("/profile", methods=["POST"])
async def profile(request):
    if find_user(
        name=request.form["user"][0],
        password=request.form["password"][0],
    ):
        return html("<html><body>:)</body></html>")
    else:
        return html("<html><body>:(</body></html>")

if __name__ == "__main__":
    app.run(
        # debug=True,
        host="0.0.0.0",
        port=8000
    )