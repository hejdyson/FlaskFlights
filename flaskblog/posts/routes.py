# creating blueprints for better code organization
# - separate folders for different functionalities
from flask import Blueprint
# additional imports
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm


# similar to creating Flask instance
posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', category='success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)


# route to a specific post - takes post_id integer variable
@posts.route('/post/<int:post_id>')
def post(post_id):
    # get_or_404 - renders only when post exists
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, legend='New Post')


# changing or eleting specific posts - takes post_id integer variable
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # get_or_404 - renders only when post exists
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        # its already in the db - we are just updating - therefore no db.session.add
        db.session.commit()
        flash('Your post has been updated!', category='success')
        return redirect(url_for('posts.post', post_id=post.id))
    # again - populating our form with previous (current values)
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


# separate route for deleting specific posts - takes post_id integer variable
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    # get_or_404 - renders only when post exists
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='success')
    return redirect(url_for('main.home'))
