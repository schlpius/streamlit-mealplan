# Streamlit Meal Planner

A lightweight Streamlit app to sketch a meal plan and grocery list. Uses Python 3.11.

## Quick start
1. Create a virtual environment and install dependencies:
   ```sh
   make install-dev
   ```
2. Run the app:
   ```sh
   make run
   ```
3. Open the Streamlit UI at http://localhost:8501.

## Scripts
- `make run` — start Streamlit.
- `make lint` — run ruff.
- `make format` — run black.
- `make test` — run pytest.

## Configuration
- Copy `.env.example` to `.env` if you need local secrets.
- Adjust meal data in `src/mealplan/planner.py`.

## Docker (optional)
Build and run:
```sh
docker build -t mealplan .
docker run --rm -p 8501:8501 mealplan
```

## Project structure
- `src/mealplan/app.py` — Streamlit UI.
- `src/mealplan/planner.py` — meal generation helpers.
- `tests/` — basic tests.

## Notes
- Target Python: 3.11
- Lint/format config in `pyproject.toml`.
