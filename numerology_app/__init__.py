import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy globally
db = SQLAlchemy()


def register_cli(app):
    """
    Add custom Flask CLI commands.
    Example usage:
        flask create-db
    """

    @app.cli.command("create-db")
    def create_db():
        """Drop all tables and recreate them fresh."""
        from numerology_app import models  # ensure all models are loaded
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("✅ All tables dropped and recreated successfully!")


def create_app():
    """Application factory for the Numerology software."""
    app = Flask(__name__)
    app.secret_key = "supersecret"

    # -----------------------------
    # Database Configuration
    # -----------------------------
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "..", "instance", "numerology.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Import models so SQLAlchemy sees them
    from numerology_app import models

    # -----------------------------
    # Register Blueprints
    # -----------------------------
    from numerology_app.routes.numerology import numerology_bp
    from numerology_app.routes.numerology_details import numerology_details_bp
    from numerology_app.routes.auth import auth_bp # for login 
    from numerology_app.routes.home import home_bp # for the home/dashboard
    from numerology_app.routes.matchmaking import matchmaking_bp
    from numerology_app.routes.clients import clients_bp
    from numerology_app.routes.docs import docs_bp
    



    app.register_blueprint(docs_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(matchmaking_bp)
    app.register_blueprint(clients_bp)

    app.register_blueprint(auth_bp)


    app.register_blueprint(numerology_bp)
    app.register_blueprint(numerology_details_bp)

    # -----------------------------
    # Root redirect → /numerology/
    # -----------------------------
    @app.route("/")
    def home_redirect():
        from flask import session, redirect, url_for
        if "user" not in session:
            return redirect(url_for("auth.login"))
        return redirect(url_for("home.dashboard"))

    # -----------------------------
    # CLI Commands
    # -----------------------------
    register_cli(app)

    return app
