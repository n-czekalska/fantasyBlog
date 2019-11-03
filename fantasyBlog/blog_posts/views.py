from flask import render_template,url_for,redirect,request,Blueprint
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
