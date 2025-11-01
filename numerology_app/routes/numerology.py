# numerology_app/routes/numerology.py

from flask import (
    Blueprint, render_template, request, session, 
    redirect, url_for, Response, current_app, flash
)
from numerology_app.utils import numerology
from numerology_app import db
from numerology_app.models import (
    LifePath, LifeExpression, SoulUrge, BirthdayDetails, AlphabetDetails,
    RepeatingNumber, MissingNumber, KarmicLineMeaning, Client,
    LuckyDayMeaning, LuckyYearMonthMeaning
)
from datetime import datetime

numerology_bp = Blueprint("numerology", __name__, url_prefix="/numerology")

@numerology_bp.before_request
def require_login():
    """Gatekeeper for all routes in this blueprint."""
    if "user" not in session:
        flash("You must be logged in to view this page.", "error")
        return redirect(url_for("auth.login"))


@numerology_bp.route("/", methods=["GET", "POST"], endpoint="numerology_home")
def numerology_home():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        middle_name = request.form.get("middle_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        dob = request.form.get("dob", "")

        full_name = " ".join([p for p in [first_name, middle_name, last_name] if p])

        results = {
            "life_path": numerology.life_path(dob),
            "expression": numerology.expression_number(full_name, numerology.PYTHAGOREAN_MAPPING),
            "soul_urge": numerology.soul_urge(full_name),
            "birthday": numerology.birthday_number(dob),
            "alphabet": full_name[0].upper() if full_name else "—",
            "karmic_chart": numerology.karmic_chart_and_lines(dob),
            "future_prediction": numerology.future_predictions(dob),
        }

        repeat_dict = numerology.repeating_numbers(dob)
        missing_list = numerology.missing_numbers(dob)
        results["missing_repeat"] = {"repeating": repeat_dict, "missing": missing_list}

        if first_name and dob:
            existing = Client.query.filter_by(first_name=first_name, dob=dob).first()
            if not existing:
                new_client = Client(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    dob=dob
                )
                db.session.add(new_client)
                db.session.commit()

        session["numerology_input"] = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "dob": dob,
        }
        session["numerology_results"] = results

        return redirect(url_for("numerology.numerology_home"))

    results = session.get("numerology_results", {}) or {}
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template("numerology/home.html", results=results, clients=clients)

@numerology_bp.route("/clear", methods=["GET"])
def clear_session():
    """
    Clears the numerology results and input from the session and redirects
    back to the home page, effectively resetting it.
    """
    session.pop("numerology_results", None)
    session.pop("numerology_input", None)
    return redirect(url_for("numerology.numerology_home"))
# ---------------------------

def _active_lines_from_chart(karmic_chart_dict):
    """
    Returns (positive_line_codes, negative_line_codes) based on the Lo Shu chart counts.
    """
    lines = [
        ('1-2-3', [1, 2, 3]),
        ('4-5-6', [4, 5, 6]),
        ('7-8-9', [7, 8, 9]),
        ('1-4-7', [1, 4, 7]),
        ('2-5-8', [2, 5, 8]),
        ('3-6-9', [3, 6, 9]),
        ('1-5-9', [1, 5, 9]),
        ('3-5-7', [3, 5, 7]),
    ]

    chart = karmic_chart_dict.get("chart", {}) if karmic_chart_dict else {}
    def count(n):  # handles int keys and string keys
        return chart.get(n, chart.get(str(n), 0)) or 0

    positives, negatives = [], []
    for code, trio in lines:
        counts = [count(n) for n in trio]
        if all(c > 0 for c in counts):
            positives.append(code)
        if all(c == 0 for c in counts):
            negatives.append(code)
    return positives, negatives


def _fetch_lookup_details(results):
    """
    Given session['numerology_results'], fetches full text from lookup tables.
    Returns a dict with all sections ready for the report template.
    """
    if not results:
        return {}

    # Core numbers from results
    life_path_no = results.get('life_path')
    expression_no = results.get('expression')
    soul_urge_no = results.get('soul_urge')
    birthday_no = results.get('birthday')
    first_alpha = results.get('alphabet')

    # DB lookups (safe fallbacks)
    life_path = LifePath.query.filter_by(number=str(life_path_no)).first() if life_path_no else None
    life_expression = LifeExpression.query.filter_by(number=str(expression_no)).first() if expression_no else None
    soul_urge = SoulUrge.query.filter_by(number=str(soul_urge_no)).first() if soul_urge_no else None
    birthday = BirthdayDetails.query.filter_by(number=str(birthday_no)).first() if birthday_no else None
    alphabet = AlphabetDetails.query.filter_by(letter=str(first_alpha)).first() if first_alpha and first_alpha != '—' else None

    # Missing / repeating numbers
    missings = results.get('missing_repeat', {}).get('missing', []) or []
    repeating = results.get('missing_repeat', {}).get('repeating', {}) or {}

    missing_rows = []
    if missings:
        for m in missings:
            row = MissingNumber.query.filter_by(number=str(m)).first()
            missing_rows.append({
                "number": str(m),
                "details": (row.details if row and row.details else "—")
            })

    repeating_rows = []
    if repeating:
        for k, v in repeating.items():  # k is number, v is count
            row = RepeatingNumber.query.filter_by(number=str(k)).first()
            repeating_rows.append({
                "number": str(k),
                "value": v,
                "meaning": (row.meaning if row and row.meaning else "—")
            })

    # Karmic chart + lines
    karmic = results.get('karmic_chart') or {}
    pos_codes, neg_codes = _active_lines_from_chart(karmic) 

    pos_lines = []
    if pos_codes:
        pos_lines = KarmicLineMeaning.query.filter(
            KarmicLineMeaning.line_type == 'positive',
            KarmicLineMeaning.numbers.in_(pos_codes)
        ).order_by(KarmicLineMeaning.numbers).all()

    neg_lines = []
    if neg_codes:
        neg_lines = KarmicLineMeaning.query.filter(
            KarmicLineMeaning.line_type == 'negative',
            KarmicLineMeaning.numbers.in_(neg_codes)
        ).order_by(KarmicLineMeaning.numbers).all()

    return {
        "life_path_no": life_path_no,
        "expression_no": expression_no,
        "soul_urge_no": soul_urge_no,
        "birthday_no": birthday_no,
        "first_alpha": first_alpha,

        "life_path": life_path,
        "life_expression": life_expression,
        "soul_urge": soul_urge,
        "birthday": birthday,
        "alphabet": alphabet,

        "karmic": karmic,
        "positive_line_rows": pos_lines,
        "negative_line_rows": neg_lines,

        "missing_rows": missing_rows,
        "repeating_rows": repeating_rows,
    }


@numerology_bp.route("/report", methods=["GET"])
def numerology_report_html():
    """HTML preview of the report (nice for quick check / print from browser)."""
    results = session.get("numerology_results", {}) or {}
    person = session.get("numerology_input", {}) or {}
    ctx = _fetch_lookup_details(results)
    if not ctx:
        return redirect(url_for("numerology.numerology_home"))

    ctx["generated_at"] = datetime.utcnow()
    ctx["person"] = person
    return render_template("numerology/report.html", **ctx)


@numerology_bp.route("/report.pdf", methods=["GET"])
def numerology_report_pdf():
    """Download as PDF using WeasyPrint (server-side)."""
    import os
    import sys

    # Force Windows to see GTK3 runtime path
    gtk_path = r"C:\Program Files\GTK3-Runtime Win64\bin"
    if gtk_path not in os.environ["PATH"]:
        os.environ["PATH"] = gtk_path + os.pathsep + os.environ["PATH"]

    from weasyprint import HTML, CSS

    results = session.get("numerology_results", {}) or {}
    person = session.get("numerology_input", {}) or {}
    ctx = _fetch_lookup_details(results)
    if not ctx:
        return redirect(url_for("numerology.numerology_home"))

    ctx["generated_at"] = datetime.utcnow()
    ctx["person"] = person

    # Render HTML (same template as preview)
    html_str = render_template("numerology/report.html", **ctx)

    pdf = HTML(string=html_str, base_url=request.host_url).write_pdf()
    fname = f"Numerology_Report_{person.get('first_name','Client')}_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.pdf"
    return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={fname}"}
    )