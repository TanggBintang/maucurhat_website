from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, User
from routes.auth import auth
from routes.curhat import curhat_bp
from routes.api import api
from flask_cors import CORS
from markupsafe import Markup  # Tambahkan import ini


# Inisialisasi Flask
app = Flask(__name__)
app.config.from_object(Config)

# Daftarkan filter nl2br untuk Jinja2
@app.template_filter('nl2br')
def nl2br_filter(text):
    if not text:
        return ""
    return Markup(text.replace('\n', '<br>'))

# Inisialisasi database
db.init_app(app)

# Inisialisasi login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Inisialisasi CORS untuk API
CORS(app)

# Daftarkan blueprint
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(curhat_bp, url_prefix='/curhat')
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def index():
    return redirect(url_for('curhat.list'))

# Buat database dan tabel jika belum ada
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)