# init file initializes the package flaskblog
from flask import Flask
# databases
from flask_sqlalchemy import SQLAlchemy
# crypting passwords
from flask_bcrypt import Bcrypt
# importing login module
from flask_login import LoginManager
# mail extension for sending email with token to user for password reset
from flask_mail import Mail
# importing Config class from config.py
from flaskblog.config import Config



db = SQLAlchemy()
# app.app_context().push()


# handling login - crypting passwords and login manager
bcrypt = Bcrypt()
login_manager = LoginManager()
# passing function name of route - same as in url_for
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # moved from above the function - need app context to create the db
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # importing and registering blueprints from all the routes in our folders
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app