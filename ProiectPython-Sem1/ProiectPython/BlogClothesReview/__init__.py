#va contine logica din spatele aplicatiei, se va ocupa de toata partea de interconectare module
#ne va ajuta sa organizam totul
import os
from flask import Flask #am importat obiectul Flask care apartine clasei/pachetului flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__) #am creat un obiect app care apartine clasei Flask si caruia i-am pasat variabila speciala __name__, care tine numele modulului curent Python

app.config['SECRET_KEY'] = 'mysecret'



###############################################
###############SetUpDataBase###################
###############################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite') #setam conexiunea bazei de date
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db) #conetam aplicatia la baza de date

###############################################



###############################################
###############LogInConfiguration##############
###############################################

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'


###############################################




from BlogClothesReview.core.views import bp as core_bp #am importat Blueprint-ul bp definit in BlogClothesReview.core.views si l-am redenumit in core_bp
app.register_blueprint(core_bp) #am folosit functia register_blueprint pentru a inregistra blueprint-ul core ca find parte din aplicatie

from BlogClothesReview.error_pages.handlers import error_pages
app.register_blueprint(error_pages)

from BlogClothesReview.users.views import users
app.register_blueprint(users)

from BlogClothesReview.clothes_reviews.views import blog_posts
app.register_blueprint(blog_posts)