from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
import os

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# --- MODIFIED: Password Storage ---
# We will store the password in a file for persistence.
PASSWORD_FILE = "password.txt"
DEFAULT_PASSWORD = "password123" # The initial password
USERNAME = "nehasnirav"

def get_password():
    """Reads the password from the file, or creates the file with the default."""
    if not os.path.exists(PASSWORD_FILE):
        set_password(DEFAULT_PASSWORD)
    with open(PASSWORD_FILE, 'r') as f:
        return f.read().strip()

def set_password(new_password):
    """Writes the new password to the file."""
    with open(PASSWORD_FILE, 'w') as f:
        f.write(new_password)
# --- END MODIFIED SECTION ---


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # MODIFIED: Check against the password from the file
        if username == USERNAME and password == get_password():
            session["user"] = username
            return redirect(url_for("home.dashboard")) # Assumes your home route is 'home.dashboard'
        else:
            return render_template("auth/login.html", error="Invalid credentials")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))


# --- NEW ROUTE: For the modal to call ---
@auth_bp.route("/change-password", methods=["POST"])
def change_password():
    """Handles the password change request from the modal."""
    previous_password = request.form.get("previous_password")
    new_password = request.form.get("new_password")

    if not previous_password or not new_password:
        return jsonify({"success": False, "error": "All fields are required."}), 400

    # Check if the previous password is correct
    if previous_password == get_password():
        # It's correct, so set the new password
        set_password(new_password)
        return jsonify({"success": True, "message": "Password updated successfully!"})
    else:
        # It's incorrect
        return jsonify({"success": False, "error": "Incorrect previous password."}), 403