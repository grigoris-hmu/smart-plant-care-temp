from pickle import FALSE
from tokenize import String
from flask import (render_template, Blueprint, g, redirect,
                   request, current_app, abort, url_for, flash)

from SmartPlantCare.forms import SignupForm, LoginForm, NewCropForm, AccountUpdateForm
from SmartPlantCare.models import User, Crop
from flask_login import login_user, current_user, logout_user, login_required

from flask_bcrypt import Bcrypt

import secrets
from PIL import Image
import os
from datetime import datetime as dt
from flask_babel import _
from SmartPlantCare import app

multilingual = Blueprint('multilingual', __name__,
                         template_folder='templates', url_prefix='/<lang_code>')


@multilingual.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@multilingual.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@multilingual.before_request
def before_request():
    if g.lang_code not in current_app.config['LANGUAGES']:
        adapter = app.url_map.bind('')
        try:
            endpoint, args = adapter.match(
                '/en' + request.full_path.rstrip('/ ?'))
            return redirect(url_for(endpoint, **args), 301)
        except:
            abort(404)

    dfl = request.url_rule.defaults
    if 'lang_code' in dfl:
        if dfl['lang_code'] != request.full_path.split('/')[1]:
            abort(404)

### ERROR HANDLERS START ###

@app.errorhandler(404)
def page_not_found(e):
    return render_template('multilingual/404.html'), 404

@app.errorhandler(415)
def unsupported_media_type(e):
    return render_template('multilingual/415.html'), 415

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('multilingual/500.html'), 500

### ERROR HANDLERS END ###


@multilingual.route('/')
@multilingual.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': _('Beautiful day in Portland!')
        },
        {
            'author': {'username': 'Susan'},
            'body': _('The Avengers movie was so cool!')
        }
    ]
    return render_template('multilingual/index.html', title=_('Home'), user=user, posts=posts)

@multilingual.route('/login', methods=['GET','POST'])
@multilingual.route('/login/', methods=['GET','POST'])
def login_page():

    ## Έλεγχος για το αν ο χρήστης έχει κάνει login ώστε αν έχει κάνει,
    ## να μεταφέρεται στην αρχική σελίδα
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm() ## Αρχικοποίηση φόρμας Login

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        ## Ανάκτηση χρήστη από τη βάση με το email του
        ## και έλεγχος του password.
        ## Εάν είναι σωστά, γίνεται login με τη βοήθεια του Flask-Login
        ## Σε κάθε περίπτωση εμφανίζονται τα αντίστοιχα flash messages

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            flash(f"Η είσοδος του χρήστη με email: {email} στη σελίδα μας έγινε με επιτυχία.", "success")
            login_user(user, remember=form.remember_me.data)

            next_link = request.args.get("next")

            return redirect(next_link) if next_link else redirect(url_for("index"))
        else:
            flash("Η είσοδος του χρήστη ήταν ανεπιτυχής, παρακαλούμε δοκιμάστε ξανά με τα σωστά email/password.", "warning")

            #return render_template('multilingual/login.html', title=_('The Cake is a Lie'))
    return render_template('multilingual/login.html', form=form)

### Logout Page ###
#@app.route("/logout")
#@app.route("/logout/")
@multilingual.route("/logout")
@multilingual.route("/logout/")
def logout_page():

    ## Logout user
    logout_user()
    flash(_('The user has been logged out.'), 'success')
    
    ## Redirect to home page
    return redirect(url_for('multilingual.index'))






@multilingual.route('/cake', defaults={'lang_code': 'en'})
@multilingual.route('/kuchen', defaults={'lang_code': 'de'})
@multilingual.route('/πίτα', defaults={'lang_code': 'el'})
@multilingual.route('/gateau', defaults={'lang_code': 'fr'})
def cake():
    return render_template('multilingual/cake.html', title=_('The Cake is a Lie'))
