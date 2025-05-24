from nicegui import ui, app
from ui.pages import login, home
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from ui.utils.decorators import require_token

def build_ui():
    app.mount('/static', StaticFiles(directory='ui/static'), name='static')

    @ui.page("/login")
    def login_page():
        ui.add_head_html('<link rel="stylesheet" href="/static/dist/main.css">')
        ui.add_head_html('<link rel="stylesheet" href="/static/dist/login.css">')

        login.render()

    @ui.page("/")
    @require_token
    def dashboard_page(request: Request):
        token = request.cookies.get('the_nair_token')
        if not token:
            ui.navigate.to('/login')
            return

        home.render()

    return ui
