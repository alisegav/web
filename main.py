import io
from flask import Flask, make_response, request
from flask import render_template, redirect, abort
from data import db_session, news_api
from data.users import User
from data.pictures import Pictures
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)
    if __name__ == '__main__':
        app.run()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        picture = Pictures()
        img: Image.Image = Image.open(io.BytesIO(request.files['file'].read()))
        stream = io.BytesIO()
        img.save(stream, format="PNG")
        picture.content = stream.getvalue()
        db_sess.add(picture)
        db_sess.commit()
        return redirect("/formuls")
    return render_template("index.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/algebra', methods=['GET'])
@login_required
def algebra():
    return render_template("algebra.html", mainpage=True)


@app.route('/geometry', methods=['GET'])
@login_required
def geometry():
    return render_template("geometry.html", mainpage=True)


@app.route('/physics', methods=['GET'])
@login_required
def physics():
    return render_template("physics.html", mainpage=True)


@app.route('/formuls', methods=['GET'])
@login_required
def formuls():
    db_sess = db_session.create_session()
    pictures = db_sess.query(Pictures.id).all()
    return render_template("formuls.html",  mainpage=True, pictures=pictures)


@app.route('/img/<int:id>',  methods=['GET'])
def getImg(id):
    session = db_session.create_session()
    picture: Pictures = session.query(Pictures).get(id)
    if (picture):
        response = make_response(picture.content)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'inline', filename=f'img-{id}.png')
        response.headers.set('Cache-Control', 'public,max-age=31536000,immutable')
        return response
    abort(404)

main()
