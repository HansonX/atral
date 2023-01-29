from pymongo import MongoClient

from users import User, Patient, Physician
from database import Database
from forms import PatientRegistrationForm, PhysicianRegistrationForm, LoginForm

from flask import Flask
from flask import request, session
from flask import flash, redirect, url_for, render_template
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required
from markupsafe import escape


# Replace <username> and <password> with the actual username and password for your MongoDB Atlas cluster
uri = "mongodb+srv://wiremarrow:admin@cluster0.32wtvyh.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoClient using the uri
client = MongoClient(uri)

# Get a reference to the "test" database
db = client["users"]

# Get a reference to the "mycollection" collection
pat_table = db["patients"]
phys_table = db["physicians"]


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
    for phys in db.get_physician_list():
        if phys.get_username() == username:
            return phys
    return None

@app.route('/')
def index():
    print(db.get_patient_list(), db.get_physician_list())
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
    form = PatientRegistrationForm()

    if form.is_submitted():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        # accept_tos = form.accept_tos.data
        pat = Patient(username, password)
        db.add_to_patient_list(pat)
        print(db.get_patient_list())

        pat_table.insert_one({"f_name": None, "l_name": None, "username": username, "password": password, "email": email, "age": None, "height": None, "weight": None, "gender": None, "sys_bp": None, "dia_bp": None, "chol": None, "glucose": None, "is_smoker": None, "is_drinker": None, "is_active": None})

        flash('Registered successfully.')

        next = request.args.get('next')

        return redirect(next or url_for('login'))
    return render_template('./register/register.html', form=form)

@app.route('/phys-register', methods=['GET', 'POST'])
def phys_register():
    form = PhysicianRegistrationForm()

    if form.is_submitted():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        # accept_tos = form.tos.data
        phys = Physician(username, password)
        db.add_to_physician_list(phys)
        print(db.get_physician_list())

        phys_table.insert_one({"f_name": None, "l_name": None, "username": username, "password": password, "email": email, "age": None, "height": None, "weight": None, "gender": None, "sys_bp": None, "dia_bp": None, "chol": None, "glucose": None, "is_smoker": None, "is_drinker": None, "is_active": None})

        flash('Registered successfully.')

        next = request.args.get('next')

        return redirect(next or url_for('login'))
    return render_template('./phys-register/phys-register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()

    if form.is_submitted():
        username = form.username.data
        password = form.password.data

        if username in [x.username for x in db.get_patient_list()]:
            real_password = db.get_patient_list()[[x.get_username() for x in db.get_patient_list()].index(username)].get_password()
            if real_password == password:
                pat = Patient(username, password)
                login_user(pat)
                flash('Logged in successfully.')
        elif username in [x.username for x in db.get_physician_list()]:
            real_password = db.get_physician_list()[[x.get_username() for x in db.get_physician_list()].index(username)].get_password()
            if real_password == password:
                phys = Physician(username, password)
                login_user(phys)
                flash('Logged in successfully.')
        else:
            return render_template('./login/login.html', form=form)

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
