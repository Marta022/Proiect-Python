# blog_posts/views.py
from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask import abort
from flask_login import current_user,login_required
from BlogClothesReview import db
from BlogClothesReview.models import ClothesReview
from BlogClothesReview.clothes_reviews.forms import ClothesReviewForm


blog_posts = Blueprint('blog_posts',__name__)

# CREATE
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = ClothesReviewForm()

    if form.validate_on_submit():

        blog_post = ClothesReview(title=form.title.data,
                            text=form.text.data,
                            user_id=current_user.id
                            )
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('coreblueprint.index'))

    return render_template('create_review.html',form=form)




# BLOG POST (VIEW)
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = ClothesReview.query.get_or_404(blog_post_id)
    return render_template('review_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post
    )



# UPDATE
@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = ClothesReview.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = ClothesReviewForm()


    if form.validate_on_submit():

        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))

    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_review.html',title='Updating',form=form)


# DELETE
@blog_posts.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):

    blog_post = ClothesReview.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('coreblueprint.index'))
