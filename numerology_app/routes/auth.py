from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# Hardcoded credentials (you can move these to config later)
USERNAME = "admin"
PASSWORD = "password123"


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("home.dashboard"))
  # redirect to dashboard
        else:
            return render_template("auth/login.html", error="Invalid credentials")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))
