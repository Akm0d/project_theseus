from flask import Flask


class WebAppFlask(Flask):
    def __init__(self, *args, **kwargs):
        Flask.__init__(self, *args, **kwargs)


def create_app(config='WebApp.config.Config'):
    app = WebAppFlask(__name__)
    with app.app_context():
        app.config.from_object(config)

    # TODO init database

    from WebApp.admin import admin
    from WebApp.base import base
    from WebApp.register import register
    from WebApp.scoreboard import scoreboard
    from WebApp.timer import timer

    app.register_blueprint(admin)
    app.register_blueprint(base)
    app.register_blueprint(register)
    app.register_blueprint(scoreboard)
    app.register_blueprint(timer)

    return app
