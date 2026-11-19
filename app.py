import streamlit as st
from recipe_logic import find_recipes

# Page title
st.title("🍳 RecipeFinder")

st.write("Find recipes using ingredients you already have!")

# Ingredient quick selection
st.subheader("What do you have?")
st.write("Select ingredients below or enter your own.")

ingredients_options = {
    "🥩 Protein": [
        "chicken", "beef", "eggs", "shrimp"
    ],
    "🥦 Vegetables": [
        "tomato", "onion", "potato", "carrot", "broccoli", "lettuce"
        ],
    "🍚 Grains & Dairy": [
        "rice", "pasta", "bread", "milk", "cheese", "butter"
    ]
}

# Clear all selected ingredients
def clear_ingredients():
    for category in ingredients_options:
        st.session_state[category] = []

    st.session_state["manual_ingredients"] = ""

selected_ingredients = []
for category, items in ingredients_options.items():
    st.write(f"**{category}**")
    selected = st.pills(
        category,
        items,
        selection_mode="multi",
        label_visibility="collapsed",
        key=category
    )
    selected_ingredients.extend(selected)

# User input for ingredients
user_input = st.text_input(
    "Other ingredients",
    placeholder="e.g., garlic, cucumber, olive oil",
    key= "manual_ingredients"
)

# Combine selected ingredients and user input
all_ingredients = selected_ingredients.copy()

if user_input:
    all_ingredients.extend(
        item.strip()
        for item in user_input.split(",")
        if item.strip()
    )

# Remove duplicates and normalize ingredients
all_ingredients = list(dict.fromkeys(
    item.lower() for item in all_ingredients
))

ingredients = ", ".join(all_ingredients)

# Selected ingredients summay
col1, col2 = st.columns([3, 1])

with col1:
    st.write(f"**{len(all_ingredients)} Ingredients selected**")

with col2:
    st.button(
        "Clear All",
        on_click=clear_ingredients,
        disabled=len(all_ingredients) == 0
    )

# Search button
if st.button("Find Recipes"):

    if ingredients.strip():

        # Get recipe recommendations
        results, corrections = find_recipes(ingredients)

        # Show spelling correcitons
        if corrections:
            for original, corrected in corrections:
                st.info(f"Spelling corrected: {original} → {corrected}")

        if results:

            st.success(f"Found {len(results)} matching recipes!")

            st.subheader("Recommended Recipes")

            # Display recipe results
            for recipe in results:

                with st.expander(
                    f"{recipe['name']} - {recipe['match']:.0f}% Match"
                ):

                    st.write("**Required Ingredients:**")
                    st.write(", ".join(recipe["ingredients"]))

                    st.write("**Missing Ingredients:**")

                    if recipe["missing"]:
                        st.write(", ".join(recipe["missing"]))
                    else:
                        st.write("None! You have all the ingredients.")

                    st.write("**Cooking Instructions:**")
                    st.write(recipe["instructions"])

        else:
            st.warning(
                "No recipes found with at least 40% ingredient match."
            )

    else:
        st.warning("Please enter at least one ingredient.")