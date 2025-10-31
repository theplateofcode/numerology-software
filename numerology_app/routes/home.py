from flask import Blueprint, render_template, session, redirect, url_for

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def root():
    """Redirect root to login or dashboard."""
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("home.dashboard"))


@home_bp.route("/home")
def dashboard():
    """Main dashboard after login."""
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return render_template("home.html")
