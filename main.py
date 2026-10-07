import pandas as pd

recipes = pd.read_csv("recipes.csv")

print("Welcome to RecipeFinder!")

ingredients = input("Enter the ingredients you have: ")
print("You entered:", ingredients)

ingredient_list = [item.strip().lower() for item in ingredients.split(",")]
print("Ingredient list:", ingredient_list)

for index, row in recipes.iterrows():
    recipe_name = row["name"]
    recipe_ingredients = [item.strip().lower() for item in row["ingredients"].split(",")]
    missing = []
    for item in recipe_ingredients:
        if item not in ingredient_list:
            missing.append(item)
    if len(missing) == 0:
        print("You can make:", recipe_name)
    else:
        print(recipe_name,"- Missing:", missing)
     