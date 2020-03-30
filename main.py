from flask import Flask, redirect
from flask import url_for
from flask import request
from flask import render_template
from flask_login import LoginManager, login_user, login_required, logout_user
from data import db_session
from data.loginform import LoginForm
from data.users import *
from data.jobs import *
from data.add_job_form import AddJobsForm
from data.register_form import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init('db/mars_explorer.sqlite')


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init('db/mars_explorer.sqlite')
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    db_session.global_init("db/mars_explorer.sqlite")
    session = db_session.create_session()
    leaders = []
    for i in session.query(Jobs).all():
        leaders.append(session.query(User).filter(User.id == i.team_leader).first())
    jobs = session.query(Jobs).all()
    session.commit()
    return render_template('index.html', jobs=jobs, leaders=leaders)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    form = AddJobsForm()
    if form.validate_on_submit():
        session = db_session.create_session()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)



if __name__ == '__main__':
    app.debug = True
    app.run(port=5000, host='127.0.0.1')
