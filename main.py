print("Welcome to RecipeFinder!")

ingredients = input("Enter the ingredients you have: ")
print("You entered:", ingredients)

ingredient_list = [item.strip() for item in ingredients.split(",")]
print("Ingredient list:", ingredient_list)

recipes = {
    "Chicken and Rice": [ "chicken", "rice"],
    "Tomato Rice": ["tomato", "rice"],
    "Chicken Tomato": ["chicken", "tomato"],
    "Fried Rice": ["rice", "egg"],
    "Tomato Egg": ["tomato", "egg"]
}
for recipe_name, recipe_ingredients in recipes.items():
    missing = []
    for item in recipe_ingredients:
        if item not in ingredient_list:
            missing.append(item)
    if len(missing) == 0:
        print("You can make:", recipe_name)
    else:
        print(recipe_name,"- Missing:", missing)
     