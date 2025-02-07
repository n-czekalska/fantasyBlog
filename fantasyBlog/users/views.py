# users/views.py
from flask import render_template,url_for,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from fantasyBlog import db
from fantasyBlog.models import User, BlogPost
from fantasyBlog.users.forms import RegistrationForm,LoginForm,UpdateUserForm

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

        user = User.query.filter_by(username=form.username.data).first()

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

@users.route('/settings',methods=['GET','POST'])
@login_required
def settings():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.avatar.data:
            picture = form.avatar.data
            current_user.avatar = picture

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about = form.about.data
        avatar = form.avatar.data
        db.session.commit()
        return redirect(url_for('users.settings'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about.data = current_user.about
        form.avatar.data = current_user.avatar

    avatar = url_for('static',filename='avatars/'+current_user.avatar)
    return render_template('settings.html',avatar=avatar,form=form)


@users.route('/<username>')
def account(username):
    page = request.args.get('page', 1, type=int) #cycling through pages of posts
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    return render_template('account.html', blog_posts=blog_posts, user=user)