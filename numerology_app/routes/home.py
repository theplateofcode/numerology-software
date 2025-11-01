from flask import Blueprint, render_template, session, redirect, url_for, flash

home_bp = Blueprint("home", __name__)

@home_bp.before_request
def require_login():
    """Gatekeeper for all routes in this blueprint."""
    if "user" not in session:
        flash("You must be logged in to view this page.", "error")
        return redirect(url_for("auth.login"))

@home_bp.route("/")
def root():
    """Redirect root to dashboard."""
    # No login check needed here, before_request handles it.
    return redirect(url_for("home.dashboard"))

@home_bp.route("/home")
def dashboard():
    """Main dashboard after login."""
    # No login check needed here, before_request handles it.
    return render_template("home.html")