import pandas as pd
from rapidfuzz import process, fuzz

recipes = pd.read_csv("recipes.csv")

print("Welcome to RecipeFinder!")

ingredients = input("Enter the ingredients you have: ")
print("You entered:", ingredients)

ingredient_list = [item.strip().lower() for item in ingredients.split(",")]
print("Ingredient list:", ingredient_list)

# Get all ingredients from the recipes
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
print("Matched ingredients:", ingredient_list)

# Find recipes based on the matched ingredients
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

    if len(missing) == 0:
        print("You can make:", recipe_name)
    else:
        print(recipe_name, "- Missing:", missing)