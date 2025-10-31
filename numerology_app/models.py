from numerology_app import db


# -------------- Common Base ---------------- #
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), nullable=False)  # 1-9, 11, 22, 33


# -------------- LIFE PATH ---------------- #
class LifePath(db.Model):
    __tablename__ = "life_path"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), nullable=False, unique=True)

    # Time Related
    lucky_date = db.Column(db.String(50))
    lucky_years = db.Column(db.String(100))
    lucky_time = db.Column(db.String(50))
    lucky_days = db.Column(db.String(50))

    # Luck & Avoidance
    lucky_no = db.Column(db.String(10))
    lucky_color = db.Column(db.String(50))
    unlucky_color = db.Column(db.String(50))
    lucky_direction = db.Column(db.String(50))
    unlucky_direction = db.Column(db.String(50))

    # Occupational
    lucky_business = db.Column(db.Text)

    # Relationships
    lucky_marriage = db.Column(db.Text)
    unlucky_marriage = db.Column(db.Text)
    mitraank = db.Column(db.String(10))
    samaank = db.Column(db.String(10))
    satraank = db.Column(db.String(10))

    # Personality
    personality = db.Column(db.Text)
    height = db.Column(db.String(50))
    thinking = db.Column(db.Text)

    # Remedies
    planet = db.Column(db.String(50))
    illness = db.Column(db.Text)
    crystal = db.Column(db.String(50))
    mantra = db.Column(db.String(100))
    stone = db.Column(db.String(50))
    god = db.Column(db.String(50))


# -------------- LIFE EXPRESSION ---------------- #
class LifeExpression(db.Model):
    __tablename__ = "life_expression"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), nullable=False, unique=True)

    description = db.Column(db.Text)
    key_traits = db.Column(db.Text)
    shadows = db.Column(db.Text)


# -------------- SOUL URGE ---------------- #
class SoulUrge(db.Model):
    __tablename__ = "soul_urge"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), nullable=False, unique=True)
    description = db.Column(db.Text)
# -------------- BIRTHDAY DETAILS ---------------- #
# -------------- BIRTHDAY DETAILS ---------------- #
class BirthdayDetails(db.Model):
    __tablename__ = "birthday_details"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), nullable=False, unique=True)
    description = db.Column(db.Text)
# -------------- ALPHABET DETAILS ---------------- #
# -------------- ALPHABET DETAILS ---------------- #
class AlphabetDetails(db.Model):
    __tablename__ = "alphabet_details"
    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.String(2), unique=True, nullable=False)
    description = db.Column(db.Text)

# -------------- REPEATING NUMBERS ---------------- #
# -------------- REPEATING NUMBERS ---------------- #
class RepeatingNumber(db.Model):
    __tablename__ = "repeating_numbers"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    repetitions = db.Column(db.Integer, nullable=False)  # e.g., 1, 2, 3, 4
    meaning = db.Column(db.Text)

    # Ensures you can't have two entries for "Number 8, 3 times"
    __table_args__ = (db.UniqueConstraint('number', 'repetitions', name='_number_repetitions_uc'),)

# -------------- MISSING NUMBERS ---------------- #
class MissingNumber(db.Model):
    __tablename__ = "missing_numbers"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), nullable=False)
    details = db.Column(db.Text)  # interpretation of missing energy or lesson



# -------------- KARMIC CHART ---------------- #
# class KarmicChartDetails(db.Model):
#     __tablename__ = "karmic_chart_details"
#     id = db.Column(db.Integer, primary_key=True)
#     number = db.Column(db.String(5))
#     description = db.Column(db.Text)
#     positive_lines = db.Column(db.Text)
#     negative_lines = db.Column(db.Text)

# -------------- KARMIC LINE MEANING ---------------- #
class KarmicLineMeaning(db.Model):
    __tablename__ = "karmic_line_meaning"
    id = db.Column(db.Integer, primary_key=True)
    
    # The name of the line, e.g., "Golden Line"
    line_name = db.Column(db.String(100), nullable=False)
    
    # The numbers in the line, e.g., "4-5-6"
    numbers = db.Column(db.String(20), nullable=False, unique=True)
    
    # 'positive' or 'negative'
    line_type = db.Column(db.String(20), nullable=False) 
    
    description = db.Column(db.Text)

from datetime import datetime

class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.String(20), nullable=False)
    results = db.Column(db.JSON)  # Store computed numerology results
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join([p for p in parts if p])


### FUTURE PREDICTIONS
# -------------- LUCKY DAY MEANING ---------------- #
class LuckyDayMeaning(db.Model):
    __tablename__ = "lucky_day_meaning"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), nullable=False, unique=True)
    description = db.Column(db.Text)
    color = db.Column(db.String(100)) # For the new color data

# -------------- LUCKY YEAR/MONTH MEANING ---------------- #
class LuckyYearMonthMeaning(db.Model):
    __tablename__ = "lucky_year_month_meaning"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(5), nullable=False, unique=True)
    description = db.Column(db.Text) # Renamed from 'meaning' for clarity