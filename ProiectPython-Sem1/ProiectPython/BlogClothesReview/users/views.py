#vom avea nevoie de un view pentru parte de register
#un view pentru partea de login
#unul pentru partea de loggout
#altul pentru partea de profil, de unde sa isi faca modificari pe profil
#si unul pentru a vedea toata lista de postari/review-uri 

from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from BlogClothesReview import db
from BlogClothesReview.models import User, ClothesReview
from BlogClothesReview.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from BlogClothesReview.users.picture_handler import add_profile_pic



users = Blueprint('users',__name__)



##########REGISTER###################
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash('Multumesc pentru inregistrare')
        return redirect(url_for('users.login'))
    
    return render_template('register.html',form=form)


##########LOGIN######################
@users.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()  #create login form
    if form.validate_on_submit(): #daca form-ul este valid la submitere

        user = User.query.filter_by(email=form.email.data).first() #salvam userul intr-o variabila dupa efectuand o cautare dupa email

        if user.check_password(form.password.data) and user is not None: #verificam daca au introdus parola corecta si daca userul exista

            login_user(user) #logam userul daca afirmatia anterioara este adevarata
            flash('LogIn efectuat cu succes')

            next = request.args.get('next') #userul incearca sa acceseze o alta pagin web care are nevoie de login, daca da fa un get pe request-ul respectiv

            if next == None or not next[0]=='/':
                next = url_for('coreblueprint.index')
            
            return redirect(next)
        
    return render_template('login.html',form=form)


##########LOGOUT#####################
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("coreblueprint.index"))


##########PROFILE_PAGE###############
@users.route('/account',methods=['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Detaliile contului au fost actualizate!')
        return redirect(url_for('users.account'))
    
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pictures/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image,form=form)


    

@users.route("/<username>")
def user_posts(username):
    page=request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = ClothesReview.query.filter_by(author=user).order_by(ClothesReview.date.desc()).paginate(page=page,per_page=5) #filtram postarile dupa autoe si de ordoman descrescator dupa data
    return render_template('user_review_posts.html',blog_posts=blog_posts,user=user)
    

##########REVIEWS_LIST###############