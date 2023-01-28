from users import User, Patient, Physician
from database import Database
from forms import RegistrationForm, LoginForm

from flask import Flask
from flask import request, session
from flask import flash, redirect, url_for, render_template
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required
from markupsafe import escape


db = Database()

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = 'amble'

login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    for pat in db.get_patient_list():
        if pat.get_username() == username:
            return pat
    return None

@app.route('/')
def index():
    return 'This is the index page'

# @app.route('/')
# def index():
#     if 'username' in session:
#         return f'Logged in as {session["username"]}'
#     return 'You are not logged in'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     elif request.method == 'GET':
#         return '''
#             <form method="post">
#                 <p><input type=text name=username>
#                 <p><input type=text name=password>
#                 <p><input type=submit value=Login>
#             </form>
#         '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # accept_tos = form.tos.data
        pat = Patient(username, password)
        db.add_to_patient_list(pat)

        flash('Registered successfully.')

        next = request.args.get('next')

        return redirect(next or url_for('index'))
    return render_template('./register/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(username, password)

        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')

        return redirect(next or url_for('index'))
    return render_template('./login/login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()

    next = request.args.get('next')

    return redirect(next or url_for('index'))

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))

# @app.route('/user/<username>')
# def patient(username):
#     # show the patient profile for that user
#     return f'User {escape(username)}'
