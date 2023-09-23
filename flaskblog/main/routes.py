# creating Blueprints for better code organization
# - separate folders for different functionalities
from flask import Blueprint
# additional imports
from flask import render_template, request
from flaskblog.models import Post



# similar to creating Flask instance
main = Blueprint('main', __name__)


@main.route('/')
def home():
    # default page is one, default type int - must be passed a number
    page = request.args.get('page', 1, type=int)
    # before - query all - now more posts so lets work with pages - paginate(), per_page - how many on page - now 5
    # .date_posted.desc()) - descending order of date - new posts show first
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)    # first post is passed to home html    second post is data from here


@main.route('/about')
def about():
    return render_template('about.html', title='About')


