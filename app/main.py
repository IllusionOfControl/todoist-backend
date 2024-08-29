from core.application import Application


def get_application() -> Application:
    return Application()


application = get_application()
app = application.fastapi_app
