import math
import pandas as pd
import streamlit as st
from dataclasses import dataclass
from typing import Literal
import random
from datetime import datetime, timedelta
import uuid

st.set_page_config(page_title="Vegetarischer Wochen-Ernährungsplan", layout="wide")

# Custom styling for better UX - Green Theme
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #27ae60;
        margin-bottom: 30px;
        font-size: 2.5em;
    }
    .info-box {
        background-color: #d5f4e6;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #27ae60;
    }
    .step-box {
        background-color: #eafaf1;
        padding: 15px;
        border-left: 4px solid #27ae60;
        margin: 10px 0;
    }
    [data-testid="stMarkdownContainer"] h2 {
        color: #27ae60;
        border-bottom: 3px solid #27ae60;
        padding-bottom: 10px;
    }
    [data-testid="stMarkdownContainer"] h3 {
        color: #229954;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Einstellungen: Aktivitätslevel -> TDEE Skalierung
# -----------------------------
CAL_TARGETS = {
    "Sedentary (×1.2)": 1750,
    "Lightly active (×1.4)": 2050,
    "Moderately active (×1.6)": 2350,
    "Very active (×1.8)": 2600,
}
BASE = 2350  # "Moderately active" als Referenz


def scale_factor(level_label: str) -> float:
    return CAL_TARGETS[level_label] / BASE


# Recipe Dataclass
MealType = Literal["breakfast", "snack", "lunch", "dinner"]


@dataclass(frozen=True)
class Recipe:
    name: str
    meal_type: MealType
    ingredients: list[tuple[str, float, str]]
    kcal: int
    tags: set[str]


# -----------------------------
# Gemüse-Basis Mix (wird auf Einzelzutaten expandiert)
# -----------------------------
VEG_MIXES = {
    "MIX_A": ["Paprika", "Karotte", "Zucchini", "Tomate"],
    "MIX_B": ["Brokkoli", "Spinat", "Erbsen", "Grüne Bohnen"],
    "MIX_C": ["Blumenkohl", "Pilze", "Rotkohl", "Frühlingszwiebel"],
}


# -----------------------------
# Runden für Handhabbarkeit
# -----------------------------
ROUNDING = {
    # Stück (robust, alltagstauglich)
    "Ei": ("piece", 1.0),
    "Brötchen": ("piece", 1.0),
    "Banane": ("piece", 1.0),
    "Apfel": ("piece", 1.0),
    "Avocado": ("piece", 0.5),
    "Gyoza": ("piece", 2.0),  # oft Packungsweise, hier auf 2er Schritte runden
}


def round_qty(ingredient: str, qty: float, unit: str) -> float:
    if unit == "piece":
        step = ROUNDING.get(ingredient, ("piece", 1.0))[1]
        return max(step, round(qty / step) * step)
    # Gramm/ml: auf praktikable Schritte runden
    if unit in ("g", "ml"):
        step = 5 if unit == "g" else 10
        return max(step, round(qty / step) * step)
    return qty


def fmt(qty: float, unit: str) -> str:
    if unit == "piece":
        if abs(qty - int(qty)) < 1e-9:
            return f"{int(qty)}"
        return f"{qty:.1f}".rstrip("0").rstrip(".")
    if unit in ("g", "ml"):
        if abs(qty - int(qty)) < 1e-9:
            return f"{int(qty)} {unit}"
        return f"{qty:.0f} {unit}"
    return f"{qty} {unit}"


SPOON_FRIENDLY = {
    "Honig",
    "Erdnussbutter",
    "Mandelmus",
    "Olivenöl",
    "Soja Sauce",
    "Sesam",
    "Currypaste",
    "Leinsamen",
    "Nüsse",
    "Zimt",
    "Hummus",
}

# Zutaten, die praktischer in Stück/Dosen statt Gramm sind (für Handling)
PIECE_HINTS_G_PER_UNIT = {
    "Blumenkohl": 400,
    "Brokkoli": 300,
    "Karotte": 80,
    "Erbsen": 150,
    "Grüne Bohnen": 120,
    "Kidneybohnen": 240,  # übliche Abtropfmenge Dose
    "Bohnen": 120,
    "Schnittkäse": 30,    # Scheibe
    "Feta": 50,
}


def normalize_ing_name(name: str) -> str:
    """Normalize ingredient naming for clarity in lists."""
    if name == "Tomate":
        return "Tomate (frisch)"
    return name


def spoon_display(ingredient: str, qty: float, unit: str) -> str | None:
    """Convert kleine Mengen in TL/EL (nur für schwer abwiegbares Kleinkram)."""
    if ingredient not in SPOON_FRIENDLY:
        return None
    if unit not in ("g", "ml"):
        return None
    if qty < 15:
        spoons = max(1, round(qty / 5))
        return f"{spoons} TL"
    if qty < 100:
        spoons = max(1, round(qty / 15))
        return f"{spoons} EL"
    return None


def piece_hint_display(ingredient: str, qty: float, unit: str) -> str | None:
    """Zeige grob in Stück/Dose für einfaches Handling, wenn in der Hint-Liste."""
    if unit != "g":
        return None
    grams_per_unit = PIECE_HINTS_G_PER_UNIT.get(ingredient)
    if not grams_per_unit:
        return None
    pieces = max(1, round(qty / grams_per_unit))
    return f"{pieces} Stk (~{grams_per_unit}g/Stk)"


def display_qty(qty: float, unit: str) -> str:
    spoon = spoon_display("", qty, unit)
    return spoon if spoon else fmt(qty, unit)


# --- Rezepte (Portionen für "moderately active")
# Ziel: ~15 min, einfache Zutaten
# ---
RECIPE_LIBRARY: list[Recipe] = [

    # ---------- FRÜHSTÜCK ----------
    Recipe(
        "Skyr-Bowl (Banane, Beeren, Nüsse, Honig)",
        "breakfast",
        [("Skyr",300,"g"),("Banane",1,"piece"),("Beeren TK",150,"g"),
         ("Nüsse",25,"g"),("Honig",15,"g"),("Leinsamen",10,"g")],
        620,
        {"high_protein","fruit","healthy_fats"},
    ),
    Recipe(
        "Brötchen-Avocado-Ei-Käse",
        "breakfast",
        [("Brötchen",2,"piece"),("Avocado",1,"piece"),("Ei",2,"piece"),
         ("Schnittkäse",40,"g"),("Tomate",1,"piece")],
        800,
        {"high_protein","healthy_fats"},
    ),
    Recipe(
        "Hafer-PB-Bowl",
        "breakfast",
        [("Haferflocken",70,"g"),("Milch",250,"ml"),
         ("Erdnussbutter",20,"g"),("Banane",1,"piece"),("Zimt",1,"g")],
        620,
        {"wholegrain","healthy_fats"},
    ),
    Recipe(
        "Overnight-Oats Skyr-Beeren",
        "breakfast",
        [("Haferflocken",70,"g"),("Skyr",250,"g"),
         ("Beeren TK",150,"g"),("Leinsamen",10,"g"),("Honig",10,"g")],
        590,
        {"wholegrain","high_protein","mealprep"},
    ),
    Recipe(
        "Tofu-Rührei + Brötchen",
        "breakfast",
        [("Tofu",150,"g"),("Zwiebel",0.5,"piece"),
         ("Gemüse MIX_B",120,"g"),("Olivenöl",10,"g"),
         ("Brötchen",1,"piece")],
        480,
        {"high_protein","veg"},
    ),

    # ---------- SNACKS ----------
    Recipe("Proteinshake","snack",
        [("Proteinpulver",30,"g"),("Sojamilch",300,"ml"),("Beeren TK",150,"g")],
        320,
        {"high_protein"}),

    Recipe("Apfel + Mandelmus","snack",
        [("Apfel",1,"piece"),("Mandelmus",20,"g")],
        220,
        {"fruit","healthy_fats"}),

    Recipe("Skyr + Honig","snack",
        [("Skyr",250,"g"),("Honig",10,"g")],
        190,
        {"high_protein"}),

    Recipe("Nüsse + Banane","snack",
        [("Nüsse",25,"g"),("Banane",1,"piece")],
        250,
        {"healthy_fats","fruit"}),

    Recipe("Gemüsesticks + Hummus","snack",
        [("Gemüse MIX_A",250,"g"),("Hummus",80,"g")],
        300,
        {"legumes","fiber"}),

    Recipe("Edamame + Sojasauce + Sesam","snack",
        [("Edamame TK",250,"g"),("Soja Sauce",15,"g"),("Sesam",10,"g")],
        370,
        {"high_protein","fiber"}),

    # ---------- LUNCH (kalt/quick) ----------
    Recipe("Vollkornbrot mit Hummus & Gemüse","lunch",
        [("Vollkornbrot",2,"piece"),("Hummus",80,"g"),
         ("Gemüse MIX_A",200,"g")],
        420,
        {"cold","quick","fiber"}),

    Recipe("Vollkornbrot mit Kräuterquark & Gurke","lunch",
        [("Vollkornbrot",2,"piece"),("Kräuterquark",120,"g"),
         ("Gurke",0.5,"piece"),("Tomate",1,"piece")],
        380,
        {"cold","quick","high_protein"}),

    Recipe("Kichererbsen-Wrap (kalt)","lunch",
        [("Vollkorn-Wrap",2,"piece"),("Kichererbsen",200,"g"),
         ("Avocado",0.5,"piece"),("Gurke",0.5,"piece"),
         ("Tomate",1,"piece"),("Skyr",80,"g")],
        780,
        {"cold","legumes","high_protein","quick"}),

    Recipe("Wrap mit Hummus & Feta","lunch",
        [("Vollkorn-Wrap",2,"piece"),("Hummus",60,"g"),
         ("Feta",60,"g"),("Tomate",1,"piece"),
         ("Gurke",0.5,"piece")],
        650,
        {"cold","quick","healthy_fats"}),

    Recipe("Mediterraner Salat + Brot","lunch",
        [("Vollkornbrot",2,"piece"),("Feta",60,"g"),
         ("Gurke",1,"piece"),("Tomate",2,"piece"),
         ("Olivenöl",10,"g")],
        600,
        {"cold","quick","healthy_fats"}),

    # ---------- DINNER (hot) ----------
    Recipe("Reis-Tofu-Gemüse-Pfanne","dinner",
        [("Reis (trocken)",90,"g"),("Tofu",200,"g"),
         ("Gemüse MIX_A",300,"g"),("Soja Sauce",20,"g"),
         ("Kimchi",80,"g"),("Olivenöl",10,"g")],
        800,
        {"hot","high_protein","veg","fermented"}),

    Recipe("Quinoa-Tofu-Bowl","dinner",
        [("Quinoa (trocken)",90,"g"),("Tofu",200,"g"),
         ("Gemüse MIX_B",300,"g"),("Soja Sauce",20,"g"),
         ("Kimchi",80,"g"),("Sesam",10,"g")],
        780,
        {"hot","high_protein","wholegrain","veg","fermented"}),

    Recipe("Linsennudeln Tomate-Spinat","dinner",
        [("Linsennudeln",120,"g"),("Tomaten (Dose)",300,"g"),
         ("Spinat (TK)",200,"g"),("Schnittkäse",30,"g"),
         ("Olivenöl",10,"g"),("Zwiebel",1,"piece"),("Knoblauch",1,"piece")],
        740,
        {"hot","legumes","high_protein","veg"}),

    Recipe("Kichererbsen-Curry + Reis","dinner",
        [("Reis (trocken)",90,"g"),("Kichererbsen",240,"g"),
         ("Tomaten (Dose)",200,"g"),("Spinat (TK)",150,"g"),
         ("Kokosmilch",200,"ml"),("Currypaste",20,"g")],
        1050,
        {"hot","legumes","veg","high_protein"}),

    Recipe("Kimchi-Fried-Rice","dinner",
        [("Reis (trocken)",90,"g"),("Ei",2,"piece"),
         ("Gemüse MIX_C",300,"g"),("Kimchi",120,"g"),
         ("Soja Sauce",15,"g"),("Olivenöl",10,"g")],
        700,
        {"hot","high_protein","veg","fermented"}),

    Recipe("Mediterrane Quinoa-Bowl","dinner",
        [("Quinoa (trocken)",90,"g"),("Feta",80,"g"),
         ("Gurke",1,"piece"),("Tomate",2,"piece"),
         ("Olivenöl",10,"g"),("Zitrone",0.5,"piece")],
        690,
        {"hot","wholegrain","veg","high_protein","healthy_fats"}),

    Recipe("Bohnen-Mais-Tacos","dinner",
        [("Vollkorn-Wrap",2,"piece"),("Kidneybohnen",220,"g"),
         ("Mais",150,"g"),("Salsa",100,"g"),
         ("Skyr",120,"g"),("Avocado",0.5,"piece")],
        900,
        {"hot","legumes","veg","high_protein"}),

    # ---------- SOUPS / STEWS (hot) ----------
    Recipe("Linsensuppe mit Gemüse","dinner",
        [("Linsen (trocken)",100,"g"),("Gemüse MIX_B",300,"g"),
         ("Kartoffel",200,"g"),("Zwiebel",1,"piece"),
         ("Olivenöl",10,"g"),("Gemüsebrühe",500,"ml")],
        680,
        {"hot","soup_stew","fiber","legumes"}),

    Recipe("Kartoffel-Lauch-Suppe","dinner",
        [("Kartoffel",300,"g"),("Lauch",150,"g"),
         ("Milch",150,"ml"),("Olivenöl",10,"g"),
         ("Gemüsebrühe",500,"ml")],
        480,
        {"hot","soup_stew","quick"}),

    Recipe("Chili sin Carne","dinner",
        [("Kidneybohnen",240,"g"),("Mais",150,"g"),
         ("Tomaten (Dose)",300,"g"),("Paprika",1,"piece"),
         ("Zwiebel",1,"piece"),("Olivenöl",10,"g")],
        700,
        {"hot","soup_stew","legumes"}),

    Recipe("Gemüse-Kichererbsen-Eintopf","dinner",
        [("Kichererbsen",200,"g"),("Gemüse MIX_A",300,"g"),
         ("Kartoffel",200,"g"),("Olivenöl",10,"g"),
         ("Gemüsebrühe",500,"ml")],
        660,
        {"hot","soup_stew","legumes","fiber"}),
]


def choose_snacks(snacks: list[Recipe], target_kcal: int, base_kcal: int) -> tuple[Recipe, Recipe]:
    """Pick two snacks to get close to the daily calorie target."""
    best_pair = None
    best_diff = None
    for s1 in snacks:
        for s2 in snacks:
            total = base_kcal + s1.kcal + s2.kcal
            diff = abs(target_kcal - total)
            if best_diff is None or diff < best_diff:
                best_diff = diff
                best_pair = (s1, s2)
    return best_pair if best_pair else (random.choice(snacks), random.choice(snacks))


def generate_weekly_plan(week_number: int) -> dict[str, dict[str, Recipe]]:
    """Generate a deterministic weekly meal plan with cold lunches and hot dinners."""
    days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

    breakfast_recipes = [r for r in RECIPE_LIBRARY if r.meal_type == "breakfast"]
    snack_recipes = [r for r in RECIPE_LIBRARY if r.meal_type == "snack"]
    lunch_recipes = [r for r in RECIPE_LIBRARY if r.meal_type == "lunch" and "cold" in r.tags]
    dinner_hot = [r for r in RECIPE_LIBRARY if r.meal_type == "dinner" and "hot" in r.tags]
    dinner_soups = [r for r in dinner_hot if "soup_stew" in r.tags]
    dinner_other = [r for r in dinner_hot if "soup_stew" not in r.tags]

    plan: dict[str, dict[str, Recipe]] = {}
    random.seed(week_number)

    soup_days = set(random.sample(days, k=2)) if len(dinner_soups) >= 2 else set()

    for day in days:
        breakfast = random.choice(breakfast_recipes)
        lunch = random.choice(lunch_recipes) if lunch_recipes else random.choice(breakfast_recipes)

        if day in soup_days and dinner_soups:
            dinner = random.choice(dinner_soups)
        else:
            dinner = random.choice(dinner_other or dinner_soups)

        base_kcal = breakfast.kcal + lunch.kcal + dinner.kcal
        snack1, snack2 = choose_snacks(snack_recipes, BASE, base_kcal)

        plan[day] = {
            "Frühstück": breakfast,
            "Snack 1": snack1,
            "Mittag": lunch,
            "Snack 2": snack2,
            "Abend": dinner,
        }

    return plan


MEAL_ORDER = ["Frühstück", "Snack 1", "Mittag", "Snack 2", "Abend"]


def expand_mix(ingredient: str, qty: float, unit: str) -> list[tuple[str, float, str]]:
    """Expandiert Gemüse MIX_* gleichmäßig auf Einzelzutaten, sonst passt durch."""
    for key, items in VEG_MIXES.items():
        if key in ingredient:
            per_item = qty / len(items)
            return [(item, per_item, unit) for item in items]
    return [(ingredient, qty, unit)]


def generate_ics_calendar(plan: dict, week_num: int, shop_df: pd.DataFrame) -> str:
    """Generate iCalendar format for Apple Reminders import."""
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Vegetarischer Ernährungsplan//EN",
        f"CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]
    
    # Assume week starts on Monday of the current year
    today = datetime.now()
    # Calculate the Monday of week_num
    jan1 = datetime(today.year, 1, 1)
    week_start = jan1 + timedelta(weeks=week_num - 1, days=-jan1.weekday())
    
    days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    
    for idx, day in enumerate(days):
        event_date = week_start + timedelta(days=idx)
        meals = plan[day]
        
        for meal_name, recipe in meals.items():
            uid = str(uuid.uuid4())
            dt_stamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
            
            # Format: YYYYMMDD
            dtstart = event_date.strftime("%Y%m%d")
            
            # Create reminder title
            title = f"{day} - {meal_name}: {recipe.name}"
            
            ics_lines.extend([
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{dt_stamp}",
                f"DTSTART;VALUE=DATE:{dtstart}",
                f"SUMMARY:{title}",
                f"DESCRIPTION:Wochenplan Woche {week_num}",
                "END:VEVENT",
            ])
    
    ics_lines.extend([
        "END:VCALENDAR",
    ])
    
    return "\n".join(ics_lines)


# UI
st.markdown("<h1 class='main-header'>🥗 Vegetarischer Wochen-Ernährungsplan</h1>", unsafe_allow_html=True)

# Instructions for beginners
with st.expander("ℹ️ Wie funktioniert diese App? (Klick zum Ausklappen)"):
    st.markdown("""
    **Diese App erstellt automatisch einen personalisierten Essensplan für dich!**
    
    1. **Woche auswählen**: Wähle, welche Woche du planen möchtest (1-52)
    2. **Aktivitätsniveau pro Tag**: Wähle für jeden Tag, wie aktiv du sein wirst
    3. **Rezepte sehen**: Alle Mahlzeiten für die Woche werden angezeigt
    4. **Einkaufsliste**: Automatisch berechnete Liste mit allen Zutaten
    5. **Download**: Speichere die Pläne als Excel oder importiere als Reminders
    
    **Aktivitätsniveaus:**
    - 🛋️ Sedentary: Wenig Bewegung (z.B. Bürojob)
    - 🚶 Lightly active: Leichte Aktivität (z.B. etwas Sport)
    - 🏃 Moderately active: Mittlere Aktivität (Standardwert)
    - 🏋️ Very active: Viel Sport und Bewegung
    """)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### 📅 Wochenauswahl")
    week_num = st.number_input("Welche Woche möchtest du planen?", min_value=1, max_value=52, value=1, help="1 = erste Woche des Jahres, 52 = letzte Woche")
with col2:
    st.markdown("### 📊 Informationen")
    st.info(
        "✅ Alle Mengen werden automatisch nach deinem Aktivitätsniveau berechnet\n\n"
        "✅ Einkaufsliste nutzt das höchste Aktivitätsniveau der Woche\n\n"
        "✅ Pro Tag nur ein warmes Gericht (Abend)\n\n"
        "✅ Mindestens 2 Suppen/Eintöpfe pro Woche\n\n"
        "✅ Rezepte sind auf ~15 Minuten ausgelegt"
    )

# Generiere Wochenplan
plan = generate_weekly_plan(week_num)

st.markdown("### 🎯 Dein Aktivitätsniveau für jeden Tag")
st.markdown("Wähle für jeden Wochentag aus, wie aktiv du sein wirst:")

days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
activity_levels = {}

cols_activity = st.columns(7)
for i, day in enumerate(days):
    with cols_activity[i]:
        activity_levels[day] = st.selectbox(
            day,
            list(CAL_TARGETS.keys()),
            index=2,
            key=f"activity_{day}",
        )

# Berechne max Faktor für Einkaufsliste
max_factor = max(scale_factor(level) for level in activity_levels.values())

# Plan-Tabelle generieren (mit pro-Tag Skalierung)
rows = []
daily_kcal = {}
for day, meals in plan.items():
    day_factor = scale_factor(activity_levels[day])
    day_total = 0
    for meal_name in MEAL_ORDER:
        recipe = meals[meal_name]
        parts = []
        for ing, qty, unit in recipe.ingredients:
            q_scaled = round_qty(ing, qty * day_factor, unit)
            for expanded_ing, expanded_qty, expanded_unit in expand_mix(ing, q_scaled, unit):
                norm_ing = normalize_ing_name(expanded_ing)
                display_piece = piece_hint_display(norm_ing, expanded_qty, expanded_unit)
                display_spoon = spoon_display(norm_ing, expanded_qty, expanded_unit)
                display = display_piece or display_spoon or fmt(expanded_qty, expanded_unit)
                parts.append(f"{norm_ing}: {display}")
        kcal_scaled = int(round(recipe.kcal * day_factor))
        day_total += kcal_scaled
        rows.append({
            "Tag": day,
            "Mahlzeit": meal_name,
            "Gericht": recipe.name,
            "Kalorien (geschätzt)": kcal_scaled,
            "Portionen/Zutaten": " | ".join(parts),
        })
    daily_kcal[day] = day_total

plan_df = pd.DataFrame(rows)

st.markdown("---")
st.markdown("## 📋 Wochenplan")
st.markdown(f"**Woche {week_num}** - Dein persönlicher Ernährungsplan für die Woche")
st.dataframe(plan_df, use_container_width=True, hide_index=True)

# Tages-Kalorien-Check
summary_rows = []
for day in days:
    target = CAL_TARGETS[activity_levels[day]]
    planned = daily_kcal.get(day, 0)
    diff = planned - target
    diff_pct = (diff / target) * 100 if target else 0
    summary_rows.append({
        "Tag": day,
        "Ziel (kcal)": target,
        "Geplant (kcal)": planned,
        "Abweichung": f"{diff:+.0f} kcal ({diff_pct:+.0f}%)",
    })

summary_df = pd.DataFrame(summary_rows)
st.markdown("### 🔎 Kalorien-Check pro Tag")
st.dataframe(summary_df, use_container_width=True, hide_index=True)

if any(abs((daily_kcal[d] - CAL_TARGETS[activity_levels[d]]) / CAL_TARGETS[activity_levels[d]]) > 0.1 for d in days):
    st.warning("Einige Tage weichen um mehr als ±10% vom Kalorienziel ab. Du kannst die Woche neu generieren, um die Schätzung zu verbessern.")
else:
    st.success("Alle Tage liegen innerhalb von ±10% des Kalorienziels.")


# Einkaufsliste aggregieren (mit max Faktor)
agg = {}

for day, meals in plan.items():
    for meal_name in MEAL_ORDER:
        recipe = meals[meal_name]
        for ing, qty, unit in recipe.ingredients:
            q_scaled = round_qty(ing, qty * max_factor, unit)
            for expanded_ing, expanded_qty, expanded_unit in expand_mix(ing, q_scaled, unit):
                norm_ing = normalize_ing_name(expanded_ing)
                key = (norm_ing, expanded_unit)
                agg[key] = agg.get(key, 0) + expanded_qty

shop_rows = []
for (ing, unit), total in sorted(agg.items(), key=lambda x: x[0][0].lower()):
    total = round_qty(ing, total, unit)
    display_piece = piece_hint_display(ing, total, unit)
    display = display_piece or spoon_display(ing, total, unit)
    shop_rows.append({
        "Zutat": ing,
        "Menge": display if display else fmt(total, unit),
        "Einheit": "" if unit == "piece" else unit,
    })

shop_df = pd.DataFrame(shop_rows)

st.markdown("---")
st.markdown("## 🛒 Einkaufsliste")
st.markdown(f"**Woche {week_num}** - Alles, was du kaufen musst (für höchstes Aktivitätsniveau)")
st.dataframe(shop_df, use_container_width=True, hide_index=True)


# Export
st.markdown("---")
st.markdown("## 💾 Download & Speichern")
st.markdown("Wähle, wie du deine Pläne speichern möchtest:")
import io

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 📊 Excel-Wochenplan")
    st.markdown("Öffne in Excel oder Google Sheets")
    buffer = io.BytesIO()
    plan_df.to_excel(buffer, index=False, engine="openpyxl")
    st.download_button(
        "⬇️ Wochenplan herunterladen",
        data=buffer.getvalue(),
        file_name=f"wochenplan_w{week_num}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

with c2:
    st.markdown("### 🛍️ Excel-Einkaufsliste")
    st.markdown("Mitnehmen beim Einkaufen")
    buffer = io.BytesIO()
    shop_df.to_excel(buffer, index=False, engine="openpyxl")
    st.download_button(
        "⬇️ Einkaufsliste herunterladen",
        data=buffer.getvalue(),
        file_name=f"einkaufsliste_w{week_num}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

with c3:
    st.markdown("### 📱 Apple Reminders")
    st.markdown("Automatische Erinnerungen in Kalender")
    ics_data = generate_ics_calendar(plan, week_num, shop_df)
    st.download_button(
        "⬇️ Zu Reminders importieren",
        data=ics_data.encode("utf-8"),
        file_name=f"wochenplan_w{week_num}.ics",
        mime="text/calendar",
    )
