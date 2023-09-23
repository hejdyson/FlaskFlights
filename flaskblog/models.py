from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin
# for generating tokens that can expire in some time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# creating user model - users on our app
# tablename automatically lowercase user - referencing in foreign key
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # post have only one author, authors have many posts - one to many relationship
    # not a column
    post = db.relationship('Post', backref='author', lazy=True)

    # methods that will generate and verify secret tokens for reseting password
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    # we dont need the instance in this method - therefore its a static method - we use the decorator
    # @staticmethod to tell python not to expect working with self
    # this method is for verifying reset token for password reset
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # ['user_id'] comes from {'user_id': self.id} above
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # dunder method (magic method) - how the object is printed when printed out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# posts on our app from users
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # default=datetime.utcnow - without brackets - passing not theevaluation of function datetime but the function itself
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # foreign key - reference to author
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # dunder method (magic method) - how the object is printed when printed out
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



# ALWAYS CRETE THE DB LIKE THIS BEFORE RUNNING THE APP
# in command line initiate the database:
# from project import app, db
# app.app_context().push()
# db.create_all()
# Then the .db file is created in a folder called "Instance" in your project. 

# creating users in terminal:
# >>> from flaskblog import User, Post
# >>> user1 = User(username='Corey', email='C@demo.com', password='password')
# >>> db.session.add(user1)
# >>> user2 = User(username='John', email='john@demo.com', password='password') 
# >>> db.session.add(user2)
# >>> db.session.commit()
# >>> User.query.all()
# [User('Corey', 'C@demo.com', 'default.jpg'), User('John', 'john@demo.com', 'default.jpg')]