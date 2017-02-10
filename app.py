# bultin library
import pprint

# external libraries
from sanic import Sanic
from sanic.response import html
from jinja2 import Environment, PackageLoader
import CRUD

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


@app.route("/sign_up", methods=['GET', 'POST'])
async def sign_up(request):
    if request.method == 'GET':
        template = env.get_template("sign_up.html")
        html_content = template.render()
        return html(html_content)
    elif request.method == 'POST':
        pprint.pprint(request.form)
        CRUD.add_user(
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
    if CRUD.find_user(
        name=request.form["user"][0],
        password=request.form["password"][0],
    ):
        return html("<html><body>:)</body></html>")
    else:
        return html("<html><body>:(</body></html>")


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
