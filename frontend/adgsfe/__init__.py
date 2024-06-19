"""
Main router definition for the ADGS Front-End application

module adgsfe
"""
# Import python utilities
import os

# Import flask utilities
from flask import Flask, send_from_directory
from flask_debugtoolbar import DebugToolbarExtension

# Import contents
from adgsfe.routers import main

def create_app():
    """
    Create and configure an instance of the Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.jinja_env.add_extension("jinja2.ext.do")

    # Get secret key
    web_server_secret_key_path = "/resources_path/web_server_secret_key.txt"
    if os.path.isfile(web_server_secret_key_path):
        web_server_secret_key_file = open(web_server_secret_key_path)
        secret_key = web_server_secret_key_file.readline().replace("\n", "")
    else:
        secret_key = os.urandom(24)
    # end if

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SECURITY_PASSWORD_SALT="ALWAYS_THE_SAME",
        SECURITY_CHANGEABLE=True,
        SECURITY_SEND_PASSWORD_CHANGE_EMAIL=False,
        SESSION_COOKIE_SECURE=False,
        REMEMBER_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True
    )

    app.register_blueprint(main.bp)
    
    if "ADGSFE_DEBUG" in os.environ and os.environ["ADGSFE_DEBUG"] == "TRUE":
        app.debug = True
        toolbar = DebugToolbarExtension(app)
    else:
        app.debug = False
    # end if
    
    # the toolbar is only enabled in debug mode:
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    # Register the specific static folder
    adgsfe_static_folder = os.path.dirname(__file__) + "/static"
    @app.route("/adgsfe_static_images/<path:filename>")
    def adgsfe_static_images(filename):
        return send_from_directory(adgsfe_static_folder + "/images", filename)
    # end def
    
    return app
