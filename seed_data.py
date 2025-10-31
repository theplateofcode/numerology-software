from numerology_app.app import create_app, db
from numerology_app.models import (
    LifePath, LifeExpression, SoulUrge,
    BirthdayDetails, AlphabetDetails,
    RepeatingNumber, MissingNumber,
    KarmicChartDetails
)

app = create_app()

with app.app_context():
    db.create_all()

    # ---------- LIFE PATH ------------
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "11", "22", "33"]
    for n in numbers:
        lp = LifePath(
            number=n,
            lucky_date="1, 10, 19, 28",
            lucky_years="19, 28, 37, 46",
            lucky_time="Morning hours",
            lucky_days="Sunday",
            lucky_no=n,
            lucky_color="Gold / Yellow",
            unlucky_color="Blue / Black",
            lucky_direction="East",
            unlucky_direction="West",
            lucky_business="Leadership, Management, Entrepreneurship",
            lucky_marriage="Compatible with 2, 3, 9",
            unlucky_marriage="Avoid 8",
            mitraank="3",
            samaank="2",
            satraank="9",
            personality=f"Sample personality traits for Life Path {n}",
            height="Average",
            thinking="Creative, forward-looking",
            planet="Sun",
            illness="Head-related issues",
            crystal="Ruby",
            mantra="Om Surya Namah",
            stone="Ruby",
            god="Surya"
        )
        db.session.add(lp)

    # ---------- EXPRESSION ----------
    for n in numbers:
        le = LifeExpression(
            number=n,
            description=f"Expression {n} represents mastery of life themes related to purpose.",
            key_traits="Charismatic, goal-driven, articulate.",
            shadows="Can become overconfident or scattered."
        )
        db.session.add(le)

    # ---------- SOUL URGE ----------
    for n in numbers:
        su = SoulUrge(
            number=n,
            description=f"Soul Urge {n} reveals deep inner motivations.",
            key_traits="Compassionate, intuitive, emotional depth.",
            shadows="Can feel misunderstood or withdrawn."
        )
        db.session.add(su)

    # ---------- BIRTHDAY DETAILS ----------
    for n in numbers:
        bd = BirthdayDetails(
            number=n,
            description=f"Birthday number {n} carries the essence of your natural gifts.",
            strength_weakness="Balanced mindset, adaptable, sometimes overthinking.",
            traits="Independent, creative, disciplined.",
            creative_artistic="Strong expression in art, writing, or music.",
            strength_responsibility="Shows leadership when focused.",
            other_traits="Friendly and open-minded."
        )
        db.session.add(bd)

    # ---------- ALPHABET DETAILS ----------
    for letter in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        ad = AlphabetDetails(
            letter=letter,
            description=f"Letter {letter} brings distinct personality influence.",
            personality_traits="Energetic, disciplined, or imaginative traits.",
            element="Air",
            vibration=5,
            ruling_planet="Mercury"
        )
        db.session.add(ad)

    # ---------- REPEATING NUMBERS ----------
    for i in range(1, 10):
        rn = RepeatingNumber(
            number=str(i),
            repeat_times=i % 3 + 1,
            details=f"Repeating number {i} signifies amplification of that vibration."
        )
        db.session.add(rn)

    # ---------- MISSING NUMBERS ----------
    for i in range(1, 10):
        mn = MissingNumber(
            number=str(i),
            details=f"Missing number {i} indicates a lesson to develop in life."
        )
        db.session.add(mn)

    # ---------- KARMIC CHART ----------
    for n in range(1, 10):
        kc = KarmicChartDetails(
            number=str(n),
            description=f"Karmic number {n} relates to inner challenges and balance.",
            positive_lines="Physical, Emotional, Mental lines complete.",
            negative_lines="Missing Creativity or Willpower line."
        )
        db.session.add(kc)

    db.session.commit()
    print("✅ Database seeded with sample numerology data.")
