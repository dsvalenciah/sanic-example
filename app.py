# external libraries
from sanic import Sanic
from sanic.response import html, redirect
from jinja2 import Environment, PackageLoader
import CRUD

env = Environment(
    loader=PackageLoader("app", "templates"),
)

app = Sanic(__name__)

app.static("/static", "./static")


@app.route("/")
async def home(request):
    template = env.get_template("home.html")
    html_content = template.render()
    return html(html_content)


@app.route("/sign_up", methods=["GET", "POST"])
async def sign_up(request):
    if request.method == "GET":
        template = env.get_template("sign_up.html")
        html_content = template.render()
        return html(html_content)
    elif request.method == "POST":
        CRUD.add_user(
            email=request.form.get("email", ""),
            name=request.form.get("user", ""),
            password=request.form.get("password", ""),
        )
        url = app.url_for("home")
        return redirect(url)


@app.route("/login", methods=["GET", "POST"])
async def login(request):
    if request.method == "GET":
        template = env.get_template("login.html")
        html_content = template.render()
        return html(html_content)
    elif request.method == "POST":
        user = CRUD.find_user(
            email_or_name=request.form.get("email_or_name", ""),
            password=request.form.get("password", ""),
        )
        if user:
            template = env.get_template("profile.html")
            html_content = template.render(name=user.name)
            return html(html_content)
        else:
            return html("<html><body>:(</body></html>")


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=8000
    )
