from users import Patient, Physician
from database import Database
from forms import PatientRegistrationForm, PhysicianRegistrationForm, LoginForm, PatientAssessmentForm, PhysicianAssessmentForm
from flask import Flask
from flask import request
from flask import redirect, url_for, render_template
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required


app = Flask(__name__)
app.secret_key = 'amble'

login_manager = LoginManager()
login_manager.init_app(app)

db = Database()


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
    for pat in [f'Patient: {x}' for x in db.get_patient_list()]:
        print(pat)
    for phys in [f'Physician: {x}' for x in db.get_physician_list()]:
        print(phys)
    return render_template('./index/index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = PatientRegistrationForm()

    if form.is_submitted():
        f_name = form.first_name.data
        l_name = form.last_name.data
        username = form.username.data
        password = form.password.data
        email = form.email.data

        if username in [x["username"] for x in db.get_patient_list()]:
            return render_template('./register/register.html', form=form)
        elif username in [x["username"] for x in db.get_physician_list()]:
            return render_template('./register/register.html', form=form)

        db.add_to_patient_list(f_name=f_name, l_name=l_name, username=username, password=password, email=email)

        next = request.args.get('next')

        return redirect(next or url_for('login'))
    return render_template('./register/register.html', form=form)


@app.route('/phys-register', methods=['GET', 'POST'])
def phys_register():
    form = PhysicianRegistrationForm()

    if form.is_submitted():
        f_name = form.first_name.data
        l_name = form.last_name.data
        username = form.username.data
        password = form.password.data
        email = form.email.data

        if username in [x["username"] for x in db.get_physician_list()]:
            return render_template('./phys-register/phys-register.html', form=form)
        elif username in [x["username"] for x in db.get_physician_list()]:
            return render_template('./phys-register/phys-register.html', form=form)

        db.add_to_physician_list(f_name=f_name, l_name=l_name, username=username, password=password, email=email)

        next = request.args.get('next')

        return redirect(next or url_for('login'))
    return render_template('./phys-register/phys-register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.is_submitted():
        username = form.username.data
        password = form.password.data

        if username in [x["username"] for x in db.get_patient_list()]:
            real_password = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["password"]
            if real_password == password:
                pat = Patient(username, password)
                login_user(pat)

                next = request.args.get('next')

                return redirect(next or url_for('portal'))
        elif username in [x["username"] for x in db.get_physician_list()]:
            real_password = db.get_physician_list()[[x["username"] for x in db.get_physician_list()].index(username)]["password"]
            if real_password == password:
                phys = Physician(username, password)
                login_user(phys)

                next = request.args.get('next')

                return redirect(next or url_for('phys_portal'))
    return render_template('./login/login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()

    next = request.args.get('next')

    return redirect(next or url_for('index'))


@app.route('/portal', methods=['GET', 'POST'])
@login_required
def portal():
    return render_template('./portal/portal.html')


@app.route('/phys-portal', methods=['GET', 'POST'])
@login_required
def phys_portal():
    return render_template('./phys-portal/phys-portal.html')


@app.route('/phys-portal-assess', methods=['GET', 'POST'])
@login_required
def phys_portal_assess():
    form = PhysicianAssessmentForm()

    if form.is_submitted():
        username = form.username.data
        sys_bp = form.sys_bp.data
        dia_bp = form.dia_bp.data
        chol = form.chol.data
        glucose = form.glucose.data
                
        if username in [x["username"] for x in db.get_patient_list()]:
            f_name = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["f_name"]
            l_name = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["l_name"]
            password = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["password"]
            email = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["email"]
            age = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["age"]
            height = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["height"]
            weight = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["weight"]
            gender = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["gender"]
            is_smoker = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["is_smoker"]
            is_drinker = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["is_drinker"]
            is_active = db.get_patient_list()[[x["username"] for x in db.get_patient_list()].index(username)]["is_active"]

            new_query = {"f_name": f_name, "l_name": l_name, "username": username, "password": password, "email": email, "age": age, "height": height, "weight": weight, "gender": gender, "sys_bp": sys_bp, "dia_bp": dia_bp, "chol": chol, "glucose": glucose, "is_smoker": is_smoker, "is_drinker": is_drinker, "is_active": is_active}
            db.update_patient_record(username, new_query)

            next = request.args.get('next')

            return redirect(next or url_for('phys_portal'))
    return render_template('./phys-portal-assess/phys-portal-assess.html', form=form)
