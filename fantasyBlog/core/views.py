from flask import render_template,request,Blueprint
from fantasyBlog.core.forms import SearchForm
from fantasyBlog.models import BlogPost


core = Blueprint('core',__name__)

@core.route('/', methods=['POST','GET'])
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    searchForm = SearchForm(request.form)
    if request.method == 'POST':
       
        blog_posts = BlogPost.query
        if searchForm.validate_on_submit():
            blog_posts = blog_posts.filter(BlogPost.title.like('%' + searchForm.data['search'] + '%'))
        blog_posts = blog_posts.order_by(BlogPost.date.desc()).paginate(page=page, per_page=4)
    
    return render_template('index.html',blog_posts=blog_posts,searchForm=searchForm)

