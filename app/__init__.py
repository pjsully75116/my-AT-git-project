from flask import Flask
from flask_login import LoginManager
import os

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = "super_secret_key"

    # ✅ Uploads folder configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # ✅ Login manager setup
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    from .routes import main
    app.register_blueprint(main)

    from .user_model import User  # ✅ Your file is user_model.py

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    return app
