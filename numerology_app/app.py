from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecret"  # replace with secure random later
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///numerology.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Import and register blueprints
    from numerology_app.routes.auth import auth_bp
    from numerology_app.routes.home import home_bp
    from numerology_app.routes.numerology import numerology_bp
    from numerology_app.routes.matchmaking import matchmaking_bp
    from numerology_app.routes.clients import clients_bp
    from numerology_app.routes.docs import docs_bp
    from numerology_app.routes.numerology_details import numerology_details_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(numerology_bp)
    app.register_blueprint(matchmaking_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(docs_bp)
    app.register_blueprint(numerology_details_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
