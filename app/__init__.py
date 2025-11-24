# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    load_dotenv()

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "changeme")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///../database/floralbot.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # ============================================================
    # ATIVAR ON DELETE CASCADE NO SQLITE
    # ============================================================
    from sqlalchemy import event
    from sqlalchemy.engine import Engine

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

    # ============================================================

    migrate.init_app(app, db)
    CORS(app)

    # ------------------------------------
    # FLASK-LOGIN
    # ------------------------------------
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"   # rota de login
    login_manager.login_message = "Você precisa estar logado para acessar esta página."

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Jinja: permite usar "agora"
    app.jinja_env.globals["now"] = datetime.utcnow

    # ------------------------------------
    # BLUEPRINTS
    # ------------------------------------
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.auth.routes import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
