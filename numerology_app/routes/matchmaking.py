from flask import Blueprint, render_template, request, flash
from numerology_app.utils import numerology
from numerology_app.models import MissingNumber, LifePath
from numerology_app import db

matchmaking_bp = Blueprint("matchmaking", __name__, url_prefix="/matchmaking")

@matchmaking_bp.route("/", methods=["GET", "POST"], endpoint="matchmaking_home")
def matchmaking_home():
    result = None

    if request.method == "POST":
        p1_name = request.form.get("p1_name", "").strip()
        p1_dob = request.form.get("p1_dob", "").strip()
        p2_name = request.form.get("p2_name", "").strip()
        p2_dob = request.form.get("p2_dob", "").strip()

        if not (p1_name and p1_dob and p2_name and p2_dob):
            flash("Please fill in both profiles.", "warning")
            return render_template("matchmaking/home.html")

        # --------------------
        # NUMEROLOGY CALCULATIONS
        # --------------------
        p1_life_path = numerology.life_path(p1_dob)
        p2_life_path = numerology.life_path(p2_dob)

        # --- Compatibility lookup ---
        compat_lookup = {
            "1": {"friends": [2, 4], "same": [1, 5, 7], "enemies": [8, 9], "god": "Surya"},
            "2": {"friends": [4, 6], "same": [2, 5, 8], "enemies": [7, 9], "god": "Chandra"},
            "3": {"friends": [6, 9], "same": [1, 2, 5, 7], "enemies": [4, 8], "god": "Vishnu"},
            "4": {"friends": [1, 8], "same": [2, 4, 6], "enemies": [3, 5, 9], "god": "Rahu"},
            "5": {"friends": [1, 3, 6, 9], "same": [2, 5, 8], "enemies": [4, 7], "god": "Mercury"},
            "6": {"friends": [3, 9], "same": [2, 5, 8], "enemies": [1, 7], "god": "Venus"},
            "7": {"friends": [2, 5], "same": [1, 4, 7], "enemies": [6, 9], "god": "Ketu"},
            "8": {"friends": [1, 4], "same": [5, 8], "enemies": [2, 3, 9], "god": "Shani"},
            "9": {"friends": [3, 6], "same": [2, 4, 5, 8], "enemies": [1, 7], "god": "Hanuman"},
        }

        def get_profile(num):
            data = compat_lookup.get(str(num), {"friends": [], "same": [], "enemies": [], "god": "-"})
            data["num"] = num
            return data

        p1 = get_profile(p1_life_path)
        p2 = get_profile(p2_life_path)

        # --------------------
        # MISSING NUMBERS (Reuse Numerology Logic)
        # --------------------
        def find_missing_numbers(name, dob):
            full_numbers = numerology.get_all_numbers_from_name_and_dob(name, dob)
            missing_list = [n for n in range(1, 10) if n not in full_numbers]

            missing_rows = MissingNumber.query.filter(
                MissingNumber.number.in_([str(m) for m in missing_list])
            ).order_by(MissingNumber.number).all()

            missing_text = ", ".join([str(m) for m in missing_list]) or "None"
            missing_details = "; ".join([f"{row.number}: {row.details}" for row in missing_rows]) or "No missing numbers."

            return missing_text, missing_details

        p1_missing_no, p1_missing_details = find_missing_numbers(p1_name, p1_dob)
        p2_missing_no, p2_missing_details = find_missing_numbers(p2_name, p2_dob)
        p1["missing_no"], p1["missing_details"] = p1_missing_no, p1_missing_details
        p2["missing_no"], p2["missing_details"] = p2_missing_no, p2_missing_details

        # --------------------
        # CRYSTAL COMBINATION (from LifePath table)
        # --------------------
        p1_crystal = None
        p2_crystal = None

        p1_life = LifePath.query.filter_by(number=str(p1_life_path)).first()
        p2_life = LifePath.query.filter_by(number=str(p2_life_path)).first()

        if p1_life and p1_life.stone:
            p1_crystal = p1_life.stone
        if p2_life and p2_life.stone:
            p2_crystal = p2_life.stone

        combined_crystals = []
        if p1_crystal:
            combined_crystals.append(p1_crystal)
        if p2_crystal and p2_crystal != p1_crystal:
            combined_crystals.append(p2_crystal)

        combined_crystal_text = " + ".join(combined_crystals) if combined_crystals else "No crystal data found."

        # --------------------
        # RELATIONSHIP TITLE
        # --------------------
        if {p1_life_path, p2_life_path} == {3, 9}:
            title = "LOVE, SACRIFICE, PURE RELATION"
        elif p1_life_path == p2_life_path:
            title = "STRONG SAME-NUMBER CONNECTION"
        elif p2_life_path in p1["friends"]:
            title = "GOOD COMPATIBILITY (Friendly Numbers)"
        elif p2_life_path in p1["enemies"]:
            title = "CHALLENGING COMPATIBILITY"
        else:
            title = "GENERAL COMPATIBILITY"

        result = {
            "title": title,
            "p1": {"name": p1_name, "dob": p1_dob, **p1},
            "p2": {"name": p2_name, "dob": p2_dob, **p2},
            "crystal_suggestion": combined_crystal_text,
        }

    return render_template("matchmaking/home.html", result=result)
