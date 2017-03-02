# external libraries
from sanic import Sanic
from sanic.response import html, redirect, text
from jinja2 import Environment, PackageLoader
import CRUD

env = Environment(
    loader=PackageLoader("app", "templates"),
)

app = Sanic(__name__)

app.static("/static", "./static")


@app.route("/")
async def start(request):
    template = env.get_template("start.html")
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
        url = app.url_for("start")
        return redirect(url)


@app.route("/login", methods=["GET", "POST"])
async def login(request):
    if request.method == "GET":
        template = env.get_template("login.html")
        html_content = template.render()
        return html(html_content)
    elif request.method == "POST":
        session = CRUD.login_user(
            email_or_name=request.form.get("email_or_name", ""),
            password=request.form.get("password", ""),
        )
        if session:
            response = redirect(app.url_for('home'))
            response.cookies['Token'] = session.token
            print(f'Aquí está!! ---------------------------{response.cookies}')
            return response
        else:
            return text(':(')


@app.route("/home")
async def home(request):
    token = request.cookies.get('Token', '')
    print('hola hola!!!!!!!!!!!!!!!')
    session, user = CRUD.get_session_by_token(token)
    print(session)
    if session:
        return text(f'{user.name} :)')
    return text(':(')


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=8000
    )
