from flask import Flask, request, g, redirect, url_for
from flask_babel import Babel
from config import Config

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)







from flask_bcrypt import Bcrypt

from flask_login import LoginManager

import os
import psycopg2

# set up application
app = Flask(__name__)
app.config.from_object(Config)

# import and register blueprints
from SmartPlantCare.blueprints.multilingual import multilingual
app.register_blueprint(multilingual)

### Configuration for Secret Key, WTF CSRF Secret Key, SQLAlchemy Database URL, 
app.config["SECRET_KEY"] = os.environ['SECRET_KEY']
app.config['WTF_CSRF_SECRET_KEY'] = os.environ['WTF_CSRF_SECRET_KEY']
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)



# set up babel
def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(
            app.config['LANGUAGES']) or app.config['LANGUAGES'][0]
    return g.lang_code

babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)

### Initialize DB and tools

#db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = "login_page"
login_manager.login_message_category = "warning"
login_manager.login_message = "Παρακαλούμε κάντε login για να μπορέσετε να δείτε αυτή τη σελίδα."
login_manager.init_app(app)

@login_manager.user_loader


#login_manager = LoginManager(app)

#login_manager.login_view = "login_page"
#login_manager.login_message_category = "warning"
#login_manager.login_message = "Παρακαλούμε κάντε login για να μπορέσετε να δείτε αυτή τη σελίδα."


#from SmartPlantCare import routes, models






    #from .models import User

@app.route('/')
def home():
    if not g.get('lang_code', None):
        get_locale()
    return redirect(url_for('multilingual.index'))
