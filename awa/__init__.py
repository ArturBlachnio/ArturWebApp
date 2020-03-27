from flask import Flask, Blueprint


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Blueprints
    from awa.main.routes import main
    app.register_blueprint(main)

    return app
