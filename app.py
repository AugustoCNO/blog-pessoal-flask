from flask import Flask
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
from models.database import db
from models.user import User


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SECRET_KEY"] = 'your_secret_key'
login_manager = LoginManager()

login_manager.init_app(app)
db.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)