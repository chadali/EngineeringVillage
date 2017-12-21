from flask import Flask
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Database").sheet1

login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object('config')

oauth = OAuth(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class MyModelView(ModelView):
    create_modal = True
    edit_modal = True
    column_default_sort = ('id', True)
    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, name='users', template_mode='bootstrap3')
from app.models import User
admin.add_view(ModelView(User, db.session))


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

login_manager.init_app(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'profile email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

with app.app_context():
        db.create_all()

from app import views