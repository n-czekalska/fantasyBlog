from flask import render_template,url_for,redirect,request,Blueprint, abort
from flask_login import login_required, current_user
from fantasyBlog import db
from fantasyBlog.models import BlogPost
from fantasyBlog.blog_posts.forms import BlogPostForm


blog_posts = Blueprint('blog_posts',__name__)

@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    
    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data,
                             content=form.content.data,
                             user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()

        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

@blog_posts.route('/<int:post_id>')
def blog_post(post_id):
    
    blog_post = BlogPost.query.get_or_404(post_id)
    return render_template('blog_post.html',title=blog_post.title,
                            date=blog_post.date,post=blog_post)

@blog_posts.route("/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def update(post_id):
    blog_post = BlogPost.query.get_or_404(post_id)
    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template('create_post.html', title='Update',
                           form=form)


@blog_posts.route("/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    blog_post = BlogPost.query.get_or_404(post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    return redirect(url_for('core.index'))