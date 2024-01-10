from BlogClothesReview import db #importam baza de date db din __ini__.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  #pt functionalitatea de login
from BlogClothesReview import login_manager #am importat login_managerul creat in __ini__.py
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)   #unique=True adica nu pot exista mai multe email-uri la fel
    username = db.Column(db.String(64),unique=True,index=True)  #index=True seteaza un index
    password_hash = db.Column(db.String(128))

    posts = db.relationship('ClothesReview',backref='author',lazy=True)  #review-ul are o relatie cu userul

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return f"Username {self.username}"

class ClothesReview(db.Model):
    
    users = db.relationship(User)  #fiecare review/postare este legata de un user 

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)  #users.id users este numele tabeleui users definita mai sus, iar id este atributul acelei tabele, nullable-False adica fiecare review/post trebuie sa aiba asoviat un user_id

    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text 
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date}  -- {self.title}"