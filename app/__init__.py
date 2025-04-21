from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev'  # Temporary secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB with app context
    db.init_app(app)

    # Register Blueprints
    from .routes.main import main
    from .routes.auth import auth
    from .routes.upload import upload
    from .routes.stats import stats
    from .routes.share import share

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(upload)
    app.register_blueprint(stats)
    app.register_blueprint(share)

    # Create database tables (only if not exist)
    with app.app_context():
        db.create_all()

    return app
