import os
import secrets
from PIL import Image
# before just app variable - now after creating function to create the app, app doesnt exist before the function,
# therefore we must use flask current_app feature
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


# saving picture
def save_picture(form_picture):
    # changing filename - generating random names for files so they dont collide with files in folder
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # i is new image created by resizing - this will be saved 
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# function for reseting password
# need flask emain extension
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='hejdyson@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, isit the following link: {url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.   
'''
# multiline string must stay at the beginning of the line
# _external = True - to show whole domain - not just relative
    mail.send(msg)