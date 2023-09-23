# creating blueprints for better code organization
# - separate folders for different functionalities
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email

# similar to creating Flask instance
users = Blueprint('users', __name__)


# we need the POST method so we can actualy submit the data in the form in this route

# instead of @app.route - in this blueprint we will use @users.route (users - name of bluprint)
@users.route('/register', methods=['GET', 'POST'])
def register():
    # first handling if current user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # form = imported created form class - from forms.py
    form = RegistrationForm()

    # validating form
    # if user with same email or same username doesnt yet exist in the database:
    if (db.session.query(User).filter_by(username=form.username.data).count() < 1 
        and db.session.query(User).filter_by(email=form.email.data).count() < 1):
        # and if form is validated on submit without errors:
        if form.validate_on_submit():
            # - if valid - generating hashed password and adding user to the database
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user1 = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user1)
            db.session.commit()
            flash(f'Your account has been created! You are able to login', category='success')
            return redirect(url_for('users.login'))
        # form = form - we need to pass the form from here to the register template we are rendering
    # else if user with same username or email already exists in the db, show message
    else:
        flash('User already exists', category='danger')
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    # first handling if current user is authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # form = imported created form class - from forms.py
    form = LoginForm()

    if form.validate_on_submit():
        # logic for login user
        user = User.query.filter_by(email=form.email.data).first()
        # check if user exists and check if password matches and if yes then login
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful', category='success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))   # ternary condition
        # if not - login unsuccessful
        else:
            flash('Login unsuccessful. Please check email and password', category='danger')

    # form = form - we need to pass the form from here to the register template we are rendering
    return render_template('login.html', title='Login', form=form)

# logout button
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


# route for users account that they can access after login
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()


    # cant set up username or email same as another which is already in the database
    # either less than 1 -- changing mail and username - cant change for mail and username which already is in the db
    # or when changing profile pic the other variables must stay same
    # this is a bad solution - better have 2 separate forms 1 for profile pic and other for email and username
    # (in tutorial this is handled in forms by validation error but it just doesnt work here)
    if ((db.session.query(User).filter_by(username=form.username.data).count() < 1 
        and db.session.query(User).filter_by(email=form.email.data).count() < 1) or
        ((current_user.username == form.username.data) 
        and (current_user.email == form.email.data))):

        if form.validate_on_submit():
            # handling picture
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated.', category='success')
            return redirect(url_for('users.account'))
        elif request.method == 'GET':
            # this should write our current user data to the form
            form.username.data = current_user.username
            form.email.data = current_user.email
    else:
        flash('User already exists.', category='danger')

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


# link when we click on username -will show user and all his posts
@users.route('/user/<string:username>')
def user_post(username):
    # default page is one, default type int - must be passed a number
    page = request.args.get('page', 1, type=int)
    # filtering user by username - get the first user - if not valid then 404 err
    user = User.query.filter_by(username=username).first_or_404() 

    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=posts, user=user)    # first post is passed to home html    second post is data from here


# enter an email for requesting password reset
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', category='info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


# here users will actually reset their password with their active token from email
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        # if token expired or invalid (verify token function returns none) - then schow message and redirect again to pw reset page
        flash('That is and invalid er expired token.', category='warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
        # and if form is validated on submit without errors:
    if form.validate_on_submit():
        # - if valid - generating hashed password and adding user to the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has ben updated! You are able to login', category='success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)