#models.py
from fantasyBlog import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):  #UserMixin.is_authenticated()

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    avatar = db.Column(db.String(64),nullable=False,default='dragon.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    about = db.Column(db.Text)
    password_hashed = db.Column(db.String(128))

    posts = db.relationship('BlogPost',backref='author',lazy=True)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hashed = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hashed,password)


class BlogPost(db.Model):
    __searchable__ = ['title']
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    content = db.Column(db.Text,nullable=False)

    def __init__(self,title,content,user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

