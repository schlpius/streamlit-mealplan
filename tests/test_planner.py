from mealplan.planner import MEAL_CATALOG, aggregate_grocery_list, generate_meal_plan


def test_generate_meal_plan_shape():
    plan = generate_meal_plan(days=2, meals_per_day=2, preference="balanced")
    assert len(plan) == 2
    assert all(len(day["meals"]) == 2 for day in plan)


def test_aggregate_grocery_list_sums_items():
    plan = generate_meal_plan(days=1, meals_per_day=2, preference="balanced")
    grocery = aggregate_grocery_list(plan)
    assert grocery
    # Ensure items are aggregated
    expected_items = {item for meal in MEAL_CATALOG["balanced"] for item in meal.ingredients}
    assert expected_items.intersection(grocery.keys())
