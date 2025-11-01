from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from numerology_app.extensions import db
from numerology_app.models import (
    LifePath, LifeExpression, SoulUrge,
    BirthdayDetails, AlphabetDetails,
    RepeatingNumber, MissingNumber,
    KarmicLineMeaning,
    LuckyYearMonthMeaning, LuckyDayMeaning
)

docs_bp = Blueprint("docs", __name__, url_prefix="/docs")

@docs_bp.before_request
def require_login():
    """Gatekeeper for all routes in this blueprint."""
    if "user" not in session:
        flash("You must be logged in to view this page.", "error")
        return redirect(url_for("auth.login"))

# A dictionary mapping table names to their models
MODEL_MAP = {
    "life_path": LifePath,
    "life_expression": LifeExpression,
    "soul_urge": SoulUrge,
    "birthday": BirthdayDetails,
    "alphabet": AlphabetDetails,
    "repeating": RepeatingNumber,
    "missing": MissingNumber,
    "karmic_lines": KarmicLineMeaning,
    "lucky_year_month": LuckyYearMonthMeaning,
    "lucky_day": LuckyDayMeaning
}

@docs_bp.route("/", methods=["GET"])
def docs_home():
    data = {
        table_name: model.query.all()
        for table_name, model in MODEL_MAP.items()
    }
    return render_template("docs.html", data=data)


@docs_bp.route("/get/<table>/<int:item_id>")
def get_entry(table, item_id):
    """AJAX endpoint to fetch a single record for editing"""
    model = MODEL_MAP.get(table)
    if not model:
        return jsonify({"error": "Table not found"}), 404
        
    record = model.query.get_or_404(item_id)
    return jsonify({col.name: getattr(record, col.name) for col in record.__table__.columns})


@docs_bp.route("/edit/<table>/<int:item_id>", methods=["POST"])
def edit_entry(table, item_id):
    model = MODEL_MAP.get(table)
    if not model:
        flash(f"Invalid table name: {table}", "error")
        return redirect(url_for("docs.docs_home"))

    record = model.query.get_or_404(item_id)
    
    for key, val in request.form.items():
        if hasattr(record, key):
            try:
                setattr(record, key, val)
            except Exception as e:
                db.session.rollback()
                flash(f"Error updating {key}: {e}", "error")
                return redirect(url_for("docs.docs_home"))
                
    try:
        db.session.commit()
        flash(f"{table.replace('_', ' ').title()} record updated successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Database error on update: {e}", "error")

    return redirect(url_for("docs.docs_home"))