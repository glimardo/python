import os
import logging

from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cache import Cache
from flask_compress import Compress

# local import
from ._config import app_config

# instantiate the extensions
login_manager = LoginManager()
bcrypt = Bcrypt()
db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})
compress = Compress()
migrate = Migrate()


def create_app(config_name):
    
    # instantiate the app
    app = Flask(
                __name__,
                template_folder='../frontend/templates',
                static_folder='../frontend/static',
                instance_relative_config=True)
    # import config
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    print("\n * Using config: " + str(config_name))

    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # set up extensions
    login_manager.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    compress.init_app(app)
    migrate.init_app(app)

    # register blueprint
    from .home.views import home_blueprint
    from .user.views import user_blueprint
    from .post.views import post_blueprint
    from .admin.views import admin_blueprint
    from .topic.views import topic_blueprint
    from .tag.view import tag_blueprint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(post_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(topic_blueprint)
    app.register_blueprint(tag_blueprint)

    # flask login
    from .models import User
    login_manager.login_view = 'user.login'
    login_manager.loging_message = "You must be logged in to access this page."
    login_manager.loging_message_category = "danger"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()
        return app

    # error handlers
    @app.errorhandler(400)
    def bad_request_page(error):
        app.logger.error('400 - Bad request page: ' + str(request.url))
        return render_template('errors/400.html'), 400

    @app.errorhandler(401)
    def unauthorized_page(error):
        app.logger.error('401 - Unauthorized page: ' + str(request.url))
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        app.logger.error('403 - Forbidden page: ' + str(request.url))
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        app.logger.error('404 - Page not found: ' + str(request.url))
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        app.logger.error('500 - Server error: ' + str(error))
        return render_template('errors/500.html'), 500

    return app
