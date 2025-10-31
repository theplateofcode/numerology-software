from flask import Blueprint, flash, redirect, render_template, session, url_for
from numerology_app.models import (
    LifePath,
    LifeExpression,
    SoulUrge,
    BirthdayDetails,
    AlphabetDetails,
    RepeatingNumber,
    MissingNumber,
    
    LuckyDayMeaning,
    LuckyYearMonthMeaning

)

numerology_details_bp = Blueprint(
    "numerology_details", __name__, url_prefix="/numerology/details"
)

# ----------------------------------------------
# Utility function: get stored session results
# ----------------------------------------------
def get_results():
    results = session.get("numerology_results")
    if not results:
        print("⚠️ No results found in session.")
    return results


# ----------------------------------------------
# LIFE PATH DETAILS
# ----------------------------------------------
@numerology_details_bp.route("/life-path/<int:number>")
def life_path_detail(number):
    data = LifePath.query.filter_by(number=str(number)).first()
    return render_template("numerology/details/life_path.html", number=number, data=data)


# ----------------------------------------------
# LIFE EXPRESSION DETAILS
# ----------------------------------------------
@numerology_details_bp.route("/life-expression/<int:number>")
def life_expression_detail(number):
    data = LifeExpression.query.filter_by(number=str(number)).first()
    return render_template("numerology/details/life_expression.html", number=number, data=data)


# ----------------------------------------------
# SOUL URGE DETAILS
# ----------------------------------------------
@numerology_details_bp.route("/soul-urge/<int:number>")
def soul_urge_detail(number):
    data = SoulUrge.query.filter_by(number=str(number)).first()
    return render_template("numerology/details/soul_urge.html", number=number, data=data)


# ----------------------------------------------
# BIRTHDAY DETAILS
# ----------------------------------------------
@numerology_details_bp.route("/birthday/<int:number>")
def birthday_detail(number):
    data = BirthdayDetails.query.filter_by(number=str(number)).first()
    return render_template("numerology/details/birthday.html", number=number, data=data)


# ----------------------------------------------
# ALPHABET DETAILS
# ----------------------------------------------
@numerology_details_bp.route("/alphabet/<string:letter>")
def alphabet_detail(letter):
    data = AlphabetDetails.query.filter_by(letter=letter.upper()).first()
    return render_template("numerology/details/alphabet.html", letter=letter.upper(), data=data)


# ----------------------------------------------
# REPEATING NUMBERS
# ----------------------------------------------
@numerology_details_bp.route("/repeating")
def repeating_detail():
    results = get_results()
    if not results:
        return render_template("numerology/details/repeating.html", repeated_data=None)

    # Get the dict of {number: count}, e.g., {1: 1, 0: 2, 7: 1}
    repeating_dict = results.get("missing_repeat", {}).get("repeating", {})
    if not repeating_dict:
        return render_template("numerology/details/repeating.html", repeated_data=None)

    # MODIFIED: This will hold the data in a more structured way
    # e.g., {1: {'count': 1, 'meanings': [obj]}, 0: {'count': 2, 'meanings': [obj, obj]}}
    template_data = {}

    for number, count in repeating_dict.items():
        try:
            num_int = int(number)
            rep_count = int(count)
        except ValueError:
            continue 

        # Query for all meanings UP TO the counted number of repetitions
        meanings = RepeatingNumber.query.filter(
            RepeatingNumber.number == num_int,
            RepeatingNumber.repetitions <= rep_count
        ).order_by(RepeatingNumber.repetitions).all()
        
        if meanings:
            # MODIFIED: Store both the real count and the list of meanings
            template_data[num_int] = {
                'count': rep_count,
                'meanings': meanings
            }

    return render_template(
        "numerology/details/repeating.html",
        repeated_data=template_data
    )
# ----------------------------------------------
# MISSING NUMBERS
# ----------------------------------------------
@numerology_details_bp.route("/missing")
def missing_detail():
    results = get_results()
    if not results:
        return render_template("numerology/details/missing.html", missing_numbers=None)

    missing_list = results.get("missing_repeat", {}).get("missing", [])
    if not missing_list:
        return render_template("numerology/details/missing.html", missing_numbers=None)

    missing_numbers = MissingNumber.query.filter(
        MissingNumber.number.in_([str(m) for m in missing_list])
    ).order_by(MissingNumber.number).all()

    return render_template("numerology/details/missing.html", missing_numbers=missing_numbers)


import re # <-- Add this import at the top of your file

# ... (other imports)

# ----------------------------------------------
# KARMIC CHART DETAILS (Positive & Negative Lines)
# ----------------------------------------------
@numerology_details_bp.route("/karmic-lines")
def karmic_lines_detail():
    from numerology_app.models import KarmicLineMeaning

    results = get_results()
    if not results or 'karmic_chart' not in results:
        flash("Please generate a report first...", "error")
        return redirect(url_for('numerology.numerology_home'))

    karmic_chart_data = results.get('karmic_chart', {})

    # --- THIS IS THE MODIFIED SECTION ---
    # Get the original lists (e.g., ['Physical Line (1-4-7)'])
    calculated_pos_full_names = karmic_chart_data.get('positive_lines', [])
    calculated_neg_full_names = karmic_chart_data.get('negative_lines', [])

    # Function to extract 'X-Y-Z' from '(X-Y-Z)' using regex
    def extract_numbers(line_name_str):
        match = re.search(r'\((\d+-\d+-\d+)\)', line_name_str)
        return match.group(1) if match else None

    # Extract only the number strings (e.g., ['1-4-7'])
    pos_number_keys = [extract_numbers(name) for name in calculated_pos_full_names if extract_numbers(name)]
    neg_number_keys = [extract_numbers(name) for name in calculated_neg_full_names if extract_numbers(name)]
    # --- END MODIFIED SECTION ---


    # Now query using the extracted number keys
    positive_lines = KarmicLineMeaning.query.filter(
        KarmicLineMeaning.numbers.in_(pos_number_keys), # <-- Use extracted keys
        KarmicLineMeaning.line_type == 'positive'
    ).all()

    negative_lines = KarmicLineMeaning.query.filter(
        KarmicLineMeaning.numbers.in_(neg_number_keys), # <-- Use extracted keys
        KarmicLineMeaning.line_type == 'negative'
    ).all()

    # --- Debugging Prints (Optional - remove after testing) ---
    print("--- Debugging Karmic Lines (After Fix) ---")
    print(f"Extracted Positive Number Keys: {pos_number_keys}")
    print(f"Extracted Negative Number Keys: {neg_number_keys}")
    print(f"Found Positive Lines from DB: {positive_lines}")
    print(f"Found Negative Lines from DB: {negative_lines}")
    print("-----------------------------------------")
    # ----------------------------------------------------

    return render_template(
        "numerology/details/karmic_lines_detail.html",
        positive_lines=positive_lines,
        negative_lines=negative_lines,
    )
# @numerology_details_bp.route("/details/karmic-chart")
# def karmic_chart_detail():
#     from numerology_app.models import KarmicChartDetails, RepeatingNumber, MissingNumber

#     # Get all karmic chart number meanings (1–9)
#     chart_data = KarmicChartDetails.query.order_by(KarmicChartDetails.number).all()
#     repeating_data = RepeatingNumber.query.all()
#     missing_data = MissingNumber.query.all()

#     return render_template(
#         "numerology/details/karmic_chart_detail.html",
#         chart_data=chart_data,
#         repeating_data=repeating_data,
#         missing_data=missing_data,
#     )



from datetime import datetime
# add missing imports


# ... (your other routes)

@numerology_details_bp.route("/future-predictions")
def future_prediction_detail():
    """
    Displays all three future prediction meanings on one page.
    """
    results = get_results() # Get calculations from the session
    if not results or 'future_prediction' not in results:
        flash("Please generate a report first.", "error")
        return redirect(url_for('numerology.numerology_home'))

    predictions = results['future_prediction']
    lucky_year_num = predictions.get('lucky_year')
    lucky_month_num = predictions.get('lucky_month')
    lucky_day_num = predictions.get('lucky_day')

    # Fetch all meanings from the database
    meanings = {
        'year': LuckyYearMonthMeaning.query.filter_by(number=str(lucky_year_num)).first(),
        'month': LuckyYearMonthMeaning.query.filter_by(number=str(lucky_month_num)).first(),
        'day': LuckyDayMeaning.query.filter_by(number=str(lucky_day_num)).first()
    }

    return render_template(
        "numerology/details/future_prediction.html",
        predictions=predictions,
        meanings=meanings,
        today_date=datetime.now().strftime("%d %B %Y")
    )