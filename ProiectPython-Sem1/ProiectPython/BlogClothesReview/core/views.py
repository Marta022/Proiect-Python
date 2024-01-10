from flask import render_template,Blueprint, request
from BlogClothesReview.models import ClothesReview

#render_template -> o functie din clasa flask care ne ajuta sa furnizam pagini HTML ca template drept raspuns pentru anumite actiuni
#Blueprint -> am importat funtia Blueprint a clasei flask

bp = Blueprint('coreblueprint',__name__) #am creat un obiect bp de tip Blueprint, caruia i-am parsat doua argumente, un nume 'coreblueprint' si variabila speciala __name__ care tine numele modulului curent de Python

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = ClothesReview.query.order_by(ClothesReview.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html',blog_posts=blog_posts) #am folosit functia render_template pentru a afisa pe ruta / un template denumit index.html

@bp.route('/info')
def info():
    return render_template('info.html')