from flask import Flask


class WebAppFlask(Flask):
    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)


def create_app(config='WebApp.config.Config'):
    app = WebAppFlask(__name__)
    with app.app_context():
        app.config.from_object(config)

    return app
