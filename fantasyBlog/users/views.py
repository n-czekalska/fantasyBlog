# users/views.py
from flask import render_template,url_for,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from fantasyBlog import db
from fantasyBlog.models import User, BlogPost
from fantasyBlog.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from fantasyBlog.users.picture_handler import add_avatar

users = Blueprint('users',__name__)

@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)



@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)

            next = request.args.get('next')

            if next ==None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@users.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            picture = add_avatar(form.picture.data,username)
            current_user.avatar = picture

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    avatar = url_for('static',filename='avatars/'+current_user.avatar)
    return render_template('account.html',avatar=avatar,form=form)

