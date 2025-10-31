from flask import Blueprint, render_template, request, redirect, url_for
from numerology_app.models import Client
from numerology_app import db # Make sure to import db

clients_bp = Blueprint("clients", __name__, url_prefix="/clients")

@clients_bp.route("/")
def clients_list():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template("clients/list.html", clients=clients)

# --- ADD THIS NEW ROUTE ---
@clients_bp.route("/edit/<int:client_id>", methods=["POST"])
def edit_client(client_id):
    """Handles the submission from the Edit Client modal."""
    client = Client.query.get_or_404(client_id)
    if client:
        client.first_name = request.form.get("first_name")
        client.middle_name = request.form.get("middle_name")
        client.last_name = request.form.get("last_name")
        client.dob = request.form.get("dob") # Assumes dob is stored as YYYY-MM-DD string
        db.session.commit()
    return redirect(url_for("clients.clients_list"))

# --- ADD THIS NEW ROUTE ---
@clients_bp.route("/delete/<int:client_id>", methods=["POST"])
def delete_client(client_id):
    """Handles the submission from the Delete Client modal."""
    client = Client.query.get_or_404(client_id)
    if client:
        db.session.delete(client)
        db.session.commit()
    return redirect(url_for("clients.clients_list"))