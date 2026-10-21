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

# Calculat match percentage
    total = len(recipe_ingredients)
    matched = total - len(missing)

    if total > 0:
        match_percentage = (matched / total) * 100
    else:
        match_percentage = 0

#    if len(missing) == 0:
#        print("You can make:", recipe_name)
#    else:
#        print(recipe_name, "- Missing:", missing)

#    print(f"Match: {match_percentage:.0f}%")

# Store recipe results
    recipe_results.append({
        "name": recipe_name,
        "match": match_percentage,
        "missing": missing
    }) 

# Sort recipes by match percentage
recipe_results.sort(
    key=lambda recipe: recipe["match"],
    reverse=True
)

print("\n===== Recipe Recommendations =====")

for index, recipe in enumerate(recipe_results, start=1):
    print(f"\n{index}. {recipe['name']}")
    print(f"   Match: {recipe['match']:.0f}%")

    if len(recipe["missing"]) == 0:
        print("   Missing ingredients: None")
    else:
        print("   Missing ingrediends:", ", ".join(recipe["missing"]))
# print(recipe_results)

# Select a recipe
choice = input("\nEnter a recipe number to view details: ")

# Get the selected recipe
selected_recipe = recipe_results[int(choice) - 1]

print("\n===== Selected Recipe =====")
print("Recipe:", selected_recipe["name"])
print(f"Match: {selected_recipe['match']:.0f}%")
print("Missing ingredients:", selected_recipe["missing"])
