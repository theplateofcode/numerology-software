from datetime import datetime

# -------------------
# Lookup Table (Pythagorean)
# -------------------
PYTHAGOREAN_MAPPING = {
    "A": 1, "J": 1, "S": 1,
    "B": 2, "K": 2, "T": 2,
    "C": 3, "L": 3, "U": 3,
    "D": 4, "M": 4, "V": 4,
    "E": 5, "N": 5, "W": 5,
    "F": 6, "O": 6, "X": 6,
    "G": 7, "P": 7, "Y": 7,
    "H": 8, "Q": 8, "Z": 8,
    "I": 9, "R": 9
}

# -------------------
# Helper Functions
# -------------------
def reduce_to_single_digit(num: int) -> int:
    """
    Reduce a number to a single digit unless it’s a master number (11, 22, 33).
    """
    while num > 9 and num not in (11, 22, 33):
        num = sum(int(d) for d in str(num))
    return num

def reduce_to_single_digit_life_path(num: int) -> int:
    """
    Reduce a number to a single digit unless it’s a master number (11, 22, 33).
    """
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num


def letters_to_numbers(name: str, mapping: dict) -> list[int]:
    """
    Convert name into list of numbers based on lookup mapping.
    Example: {"A":1, "B":2, ...}
    """
    name = name.upper()
    return [mapping.get(ch, 0) for ch in name if ch.isalpha()]

# -------------------
# Main Calculations
# -------------------
def life_path(dob: str) -> int:
    """
    Life Path = reduced (day + month + year).
    Master numbers (11, 22, 33) are not reduced.
    """
    dob_date = datetime.strptime(dob, "%Y-%m-%d")

    # Day
    day = reduce_to_single_digit(dob_date.day)

    # Month
    month = reduce_to_single_digit(dob_date.month)

    # Year (reduce year digits first, then reduce result)
    year_digits = sum(int(d) for d in str(dob_date.year))
    year = reduce_to_single_digit(year_digits)

    # Add them
    total = day + month + year
    return reduce_to_single_digit_life_path(total)


def expression_number(full_name: str, mapping: dict) -> int:
    """
    Expression (Destiny) Number calculation:
    - Split full name into parts (first, middle, last, etc.)
    - For each part:
        * Sum letter values (using Pythagorean mapping)
        * Reduce to single digit unless it's 11 or 22
    - Add reduced parts together
    - Reduce again to single digit unless it's 11 or 22
    - Return final result
    """
    name_parts = full_name.strip().upper().split()

    part_totals = []
    for part in name_parts:
        # sum values of letters in this part
        total = sum(mapping.get(ch, 0) for ch in part if ch.isalpha())

        # reduce this name part (unless 11 or 22)
        if total not in (11, 22):
            total = reduce_to_single_digit(total)

        part_totals.append(total)

    # add reduced parts
    grand_total = sum(part_totals)

    # final reduction (unless 11 or 22)
    if grand_total not in (11, 22):
        grand_total = reduce_to_single_digit(grand_total)

    return grand_total

def soul_urge(full_name: str) -> int:
    """
    Soul Urge (Heart's Desire) Number calculation (Book version):
    - Uses vowels (A=1, E=5, I=9, O=6, U=3, Y=7 when it acts as a vowel).
    - Split full name into parts (first, middle, last, etc.).
    - For each part:
        * Sum vowel values (do NOT reduce here)
    - Add all part sums together.
    - Reduce final total to a single digit, unless it's 11, 22, or 33.
    """

    vowel_mapping = {"A": 1, "E": 5, "I": 9, "O": 6, "U": 3, "Y": 7}
    name_parts = full_name.strip().upper().split()

    grand_total = 0

    for part in name_parts:
        letters = list(part)
        total = 0

        for i, ch in enumerate(letters):
            if ch in "AEIOU":
                total += vowel_mapping[ch]
            elif ch == "Y":
                # Rule: Y is vowel if no A/E/I/O/U in part OR surrounded by consonants
                if not any(v in part for v in "AEIOU"):
                    total += vowel_mapping["Y"]
                elif (i > 0 and letters[i-1] not in "AEIOU") and (i < len(letters)-1 and letters[i+1] not in "AEIOU"):
                    total += vowel_mapping["Y"]

        # Add the raw total for this part (no reduction yet)
        grand_total += total

    # Final reduction (unless master number)
    if grand_total not in (11, 22, 33):
        grand_total = reduce_to_single_digit(grand_total)

    return grand_total

def repeating_numbers(date_of_birth: str):
    """
    Returns a dictionary of all present numbers from a DOB.

    Example:
        DOB: 19-07-2004
        → returns {0: 2, 1: 1, 9: 1, 7: 1, 2: 1, 4: 1}
    """

    digits = [int(ch) for ch in date_of_birth if ch.isdigit()]
    counts = {d: digits.count(d) for d in range(0, 10)}
    
    # --- THIS IS THE FIX ---
    # Change v > 1 to v > 0 to include numbers that appear even once
    present_numbers = {k: v for k, v in counts.items() if v > 0}
    # -----------------------
    
    return present_numbers
def missing_numbers(date_of_birth: str):
    """
    Returns a list of missing numbers (1–9) after applying extended reduction logic.
    
    Enhancement:
    - While calculating grouped reductions for day, month, and year,
      any number that appears in the intermediate sums is removed from missing numbers.
    
    Example:
      DOB = "2004-11-12"
      → if day=1+2=3 and 3 is in missing numbers, it is removed.
      → if month=1+1=2 and 2 is in missing numbers, it is removed.
      → if year 2+0=2, 2+0+0=2, 2+0+0+4=6 → remove those if in missing numbers.
    """

    # --- Extract numeric digits from DOB ---
    digits = [int(ch) for ch in date_of_birth if ch.isdigit()]
    present = {d for d in digits if d != 0}
    missing = [n for n in range(1, 10) if n not in present]

    # --- Split into components ---
    try:
        year, month, day = date_of_birth.split("-")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format")

    def reduce_component(value: str) -> int:
        """Reduce a component (like day/month/year) to single digit or master number."""
        total = sum(int(ch) for ch in value if ch.isdigit())
        while total > 9 and total not in (11, 22, 33):
            total = sum(int(d) for d in str(total))
        return total

    # --- Helper to check and remove from missing list ---
    def remove_if_missing(num):
        num = int(num)
        if num in missing:
            missing.remove(num)

    # --- DAY grouped sums ---
    if len(day) > 1:
        total = 0
        for ch in day:
            total += int(ch)
            remove_if_missing(total if total <= 9 else sum(int(d) for d in str(total)))

    # --- MONTH grouped sums ---
    if len(month) > 1:
        total = 0
        for ch in month:
            total += int(ch)
            remove_if_missing(total if total <= 9 else sum(int(d) for d in str(total)))

    # --- YEAR grouped sums ---
    if len(year) > 1:
        total = 0
        for i, ch in enumerate(year):
            total += int(ch)
            reduced = total
            while reduced > 9 and reduced not in (11, 22, 33):
                reduced = sum(int(d) for d in str(reduced))
            remove_if_missing(reduced)

    # --- LIFE PATH removal (final safeguard) ---
    day_num = reduce_component(day)
    month_num = reduce_component(month)
    year_num = reduce_component(year)

    total = day_num + month_num + year_num
    while total > 9 and total not in (11, 22, 33):
        total = sum(int(ch) for ch in str(total))
    life_path = total
    remove_if_missing(life_path)

    return missing


def birthday_number(dob: str) -> int:
    """
    Birthday Number = day of birth reduced.
    Example: 25 → 2+5 = 7
    """
    day = int(dob.split("-")[2])
    return reduce_to_single_digit(day)


def alphabet_details(full_name: str, mapping: dict) -> list[tuple[str, int]]:
    """
    Return list of (letter, number) for full name.
    """
    return full_name[0].upper()

def karmic_chart_and_lines(date_of_birth: str):
    """
    Generate the Pythagorean Karmic Chart and determine Positive/Negative lines.
    Positive Line: all 3 numbers in line appear in DOB.
    Negative Line: none of the 3 numbers appear in DOB.
    Partial lines are ignored.
    """

    digits = [int(ch) for ch in date_of_birth if ch.isdigit() and ch != '0']
    chart = {i: 0 for i in range(1, 10)}
    for d in digits:
        chart[d] += 1

    # Define the 8 key lines
    lines = {
        "Physical Line (1-4-7)": [1, 4, 7],
        "Emotional Line (2-5-8)": [2, 5, 8],
        "Mental Line (3-6-9)": [3, 6, 9],
        "Creativity Line (1-2-3)": [1, 2, 3],
        "Willpower Line (4-5-6)": [4, 5, 6],
        "Intellect Line (7-8-9)": [7, 8, 9],
        "Determination Line (1-5-9)": [1, 5, 9],
        "Passion Line (3-5-7)": [3, 5, 7],
    }

    positive_lines = []
    negative_lines = []

    for name, nums in lines.items():
        present = [chart[n] > 0 for n in nums]

        if all(present):  # all digits exist
            positive_lines.append(name)
        elif not any(present):  # none exist
            negative_lines.append(name)
        # partial lines (some digits present) → ignored

    return {
        "chart": chart,
        "positive_lines": positive_lines,
        "negative_lines": negative_lines,
    }


from datetime import datetime

# --- HELPER FUNCTIONS ---

def _reduce_number(num: int) -> int:
    """Helper to reduce numbers, preserving master numbers 11, 22, 33."""
    while num > 9 and num not in (11, 22):
        num = sum(int(d) for d in str(num))
    return num

def _get_lucky_year(dob: str) -> int:
    """Calculates the Lucky Year."""
    dob_parts = dob.replace("/", "-").split("-")
    if len(dob_parts[0]) == 4:  # yyyy-mm-dd
        _, month_str, day_str = dob_parts
    else:  # dd-mm-yyyy
        day_str, month_str, _ = dob_parts
    
    reduced_day = _reduce_number(sum(int(d) for d in day_str))
    reduced_month = _reduce_number(sum(int(d) for d in month_str))
    return _reduce_number(reduced_day + reduced_month)

def _get_lucky_month(lucky_year_num: int) -> int:
    """Calculates the Lucky Month based on the Lucky Year."""
    current_month = datetime.now().month
    reduced_current_month = _reduce_number(current_month)
    return _reduce_number(lucky_year_num + reduced_current_month)

def _get_lucky_day(dob_str: str) -> int:
    """Calculates the Lucky Day based on DOB and current date."""
    current_date = datetime.now()
    
    dob_digits = [int(d) for d in dob_str if d.isdigit()]
    current_date_digits = [int(d) for d in current_date.strftime('%d%m%Y') if d.isdigit()]
    
    total_sum = sum(dob_digits) + sum(current_date_digits)
    return _reduce_number(total_sum)

# --- MAIN FUNCTION (called by your route) ---

def future_predictions(dob: str):
    """
    Calculate Future Lucky Year, Lucky Month, and Lucky Day
    by calling separate helper functions.
    """
    lucky_year = _get_lucky_year(dob)
    lucky_month = _get_lucky_month(lucky_year)
    lucky_day = _get_lucky_day(dob)

    return {
        "lucky_year": lucky_year,
        "lucky_month": lucky_month,
        "lucky_day": lucky_day
    }

def get_all_numbers_from_name_and_dob(full_name: str, dob: str) -> list[int]:
    """
    Combine all numbers derived from name (Pythagorean system)
    and from DOB (digits 1–9) for missing-number detection.

    This uses the same logic as expression_number() and missing_numbers().
    """
    numbers = set()

    # --- From DOB ---
    digits = [int(ch) for ch in dob if ch.isdigit() and ch != '0']
    numbers.update(digits)

    # --- From NAME (Pythagorean) ---
    name_numbers = letters_to_numbers(full_name, PYTHAGOREAN_MAPPING)
    numbers.update([n for n in name_numbers if 1 <= n <= 9])

    return sorted(numbers)
