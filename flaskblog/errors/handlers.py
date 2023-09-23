from flask import Blueprint, render_template

# this is instance of errors bluprint - it is imported to the central __init__.py
errors = Blueprint('errors', __name__)

# creating custom error messages
# error 404
@errors.app_errorhandler(404)
def error_404(error):
    # second return - specifying error code
    return render_template('errors/404.html'), 404

# error 403
@errors.app_errorhandler(403)
def error_403(error):
    # second return - specifying error code
    return render_template('errors/403.html'), 403

# error 500
@errors.app_errorhandler(500)
def error_500(error):
    # second return - specifying error code
    return render_template('errors/500.html'), 500