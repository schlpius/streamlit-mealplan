from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Meal:
    name: str
    meal_type: str
    ingredients: Dict[str, float]


MEAL_CATALOG: Dict[str, List[Meal]] = {
    "balanced": [
        Meal(
            name="Greek Yogurt Bowl",
            meal_type="breakfast",
            ingredients={"Greek yogurt (cup)": 1, "Berries (cup)": 1, "Granola (cup)": 0.25},
        ),
        Meal(
            name="Chicken Grain Bowl",
            meal_type="lunch",
            ingredients={
                "Chicken breast (g)": 150,
                "Quinoa (cup)": 0.75,
                "Spinach (cup)": 1,
                "Cherry tomatoes (cup)": 0.5,
            },
        ),
        Meal(
            name="Salmon and Veg",
            meal_type="dinner",
            ingredients={"Salmon fillet (g)": 160, "Broccoli (cup)": 1, "Brown rice (cup)": 0.75},
        ),
        Meal(
            name="Hummus Snack Box",
            meal_type="snack",
            ingredients={"Hummus (tbsp)": 4, "Carrot sticks (cup)": 1, "Pita (piece)": 1},
        ),
    ],
    "vegetarian": [
        Meal(
            name="Overnight Oats",
            meal_type="breakfast",
            ingredients={"Rolled oats (cup)": 0.75, "Almond milk (cup)": 1, "Chia seeds (tbsp)": 1},
        ),
        Meal(
            name="Tofu Stir-Fry",
            meal_type="dinner",
            ingredients={"Tofu (g)": 150, "Mixed vegetables (cup)": 2, "Rice noodles (cup)": 1},
        ),
        Meal(
            name="Caprese Sandwich",
            meal_type="lunch",
            ingredients={"Ciabatta roll (piece)": 1, "Mozzarella (g)": 60, "Tomato (slices)": 4, "Basil (leaves)": 6},
        ),
        Meal(
            name="Trail Mix",
            meal_type="snack",
            ingredients={"Mixed nuts (cup)": 0.5, "Dried fruit (cup)": 0.25},
        ),
    ],
    "high-protein": [
        Meal(
            name="Egg White Scramble",
            meal_type="breakfast",
            ingredients={"Egg whites (count)": 4, "Spinach (cup)": 1, "Feta (tbsp)": 2},
        ),
        Meal(
            name="Turkey Wrap",
            meal_type="lunch",
            ingredients={"Turkey slices (g)": 120, "Whole wheat wrap (piece)": 1, "Lettuce (cup)": 1, "Mustard (tbsp)": 1},
        ),
        Meal(
            name="Shrimp Tacos",
            meal_type="dinner",
            ingredients={"Shrimp (g)": 140, "Corn tortilla (piece)": 3, "Cabbage slaw (cup)": 1},
        ),
        Meal(
            name="Protein Shake",
            meal_type="snack",
            ingredients={"Protein powder (scoop)": 1, "Banana (piece)": 1, "Milk (cup)": 1},
        ),
    ],
}


def generate_meal_plan(days: int, meals_per_day: int, preference: str) -> List[Dict[str, object]]:
    """Generate a simple rotating meal plan based on preference."""
    catalog = MEAL_CATALOG.get(preference, MEAL_CATALOG["balanced"])
    plan: List[Dict[str, object]] = []

    for day in range(days):
        meals: List[Meal] = []
        for offset in range(meals_per_day):
            meal = catalog[(day + offset) % len(catalog)]
            meals.append(meal)
        plan.append({"day": day + 1, "meals": meals})

    return plan


def aggregate_grocery_list(plan: List[Dict[str, object]]) -> Dict[str, float]:
    """Aggregate ingredients across the plan."""
    grocery: Dict[str, float] = {}
    for day in plan:
        for meal in day["meals"]:
            if not isinstance(meal, Meal):
                continue
            for item, qty in meal.ingredients.items():
                grocery[item] = grocery.get(item, 0) + qty
    return dict(sorted(grocery.items()))
