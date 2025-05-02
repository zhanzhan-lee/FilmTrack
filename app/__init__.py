from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize Flask-Login globally
login_manager = LoginManager()
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
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)



    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from .routes.main import main
    from .routes.auth import auth
    from .routes.stats import stats
    from .routes.share import share
    from .routes.gear import gear
    from .routes.shooting import shooting
    from .routes.view_stats import view_stats

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(stats)
    app.register_blueprint(share)
    app.register_blueprint(gear)
    app.register_blueprint(view_stats)
    app.register_blueprint(shooting)

    # Create database tables (only if not exist)
    with app.app_context():
        db.create_all()

    return app
