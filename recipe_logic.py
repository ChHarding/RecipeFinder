import pandas as pd
from rapidfuzz import process, fuzz
from pathlib import Path


# Load recipe data
DATA_FILE = Path(__file__).parent / "recipes.csv"
recipes = pd.read_csv(DATA_FILE)


def find_recipes(ingredients, min_match=40):

    # Convert user input into a list
    ingredient_list = [
        item.strip().lower()
        for item in ingredients.split(",")
        if item.strip()
    ]

    if not ingredient_list:
        return []

    # Get all ingredients from recipes
    all_ingredients = []

    for index, row in recipes.iterrows():
        recipe_ingredients = row["ingredients"].split(",")

        for item in recipe_ingredients:
            item = item.strip().lower()

            if item not in all_ingredients:
                all_ingredients.append(item)

    # Correct possible spelling mistakes
    corrected_ingredients = []

    for item in ingredient_list:
        match = process.extractOne(
            item,
            all_ingredients,
            scorer=fuzz.ratio
        )

        if match and match[1] >= 80:
            corrected_ingredients.append(match[0])
        else:
            corrected_ingredients.append(item)

    ingredient_list = corrected_ingredients

    # Find recipes based on matched ingredients
    recipe_results = []

    for index, row in recipes.iterrows():

        recipe_name = row["name"]

        recipe_ingredients = [
            item.strip().lower()
            for item in row["ingredients"].split(",")
        ]

        missing = []

        for item in recipe_ingredients:
            if item not in ingredient_list:
                missing.append(item)

        # Calculate match percentage
        total = len(recipe_ingredients)
        matched = total - len(missing)

        if total > 0:
            match_percentage = (matched / total) * 100
        else:
            match_percentage = 0

        # Filter low-percentage matches
        if match_percentage >= min_match:

            recipe_results.append({
                "name": recipe_name,
                "match": match_percentage,
                "ingredients": recipe_ingredients,
                "missing": missing,
                "instructions": row["instructions"]
            })

    # Sort recipes by match percentage
    recipe_results.sort(
        key=lambda recipe: recipe["match"],
        reverse=True
    )

    return recipe_results