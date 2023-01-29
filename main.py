from users import Patient, Physician
from database import Database
from forms import PatientRegistrationForm, PhysicianRegistrationForm, LoginForm

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
        if pat["username"] == username:
            password = pat["password"]
            out_pat = Patient(username, password)
            return out_pat
    for phys in db.get_physician_list():
        if phys["username"] == username:
            password = phys["password"]
            out_phys = Physician(username, password)
            return out_phys
    return None

@app.route('/')
def index():
    print(db.get_patient_list())
    print(db.get_physician_list())
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
        # pat = Patient(username, password)

        db.add_to_patient_list(username=username, password=password, email=email)

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
        # phys = Physician(username, password)

        db.add_to_physician_list(username=username, password=password, email=email)

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

        if username in [x["username"] for x in db.get_patient_list()]:
            real_password = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["password"]
            if real_password == password:
                pat = Patient(username, password)
                login_user(pat)
                flash('Logged in successfully.')
                return render_template('./portal/portal.html')
        elif username in [x["username"] for x in db.get_physician_list()]:
            real_password = db.get_physician_list()[[x["username"] for x in db.get_physician_list()].index(username)]["password"]
            if real_password == password:
                phys = Physician(username, password)
                login_user(phys)
                flash('Logged in successfully.')
                return render_template('./phys-portal/phys-portal.html')
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
