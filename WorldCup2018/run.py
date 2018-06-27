from flask import Flask
from app.api import bp as api_bp
from exts import db
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(api_bp)
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

