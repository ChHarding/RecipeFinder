import streamlit as st
from recipe_logic import find_recipes

# Page title
st.title("🍳 RecipeFinder")

st.write("Find recipes using ingredients you already have!")

# Ingredient input
ingredients = st.text_input(
    "Enter your ingredients:",
    placeholder="e.g., chicken, tomato, onion"
)

# Search button
if st.button("Find Recipes"):

    if ingredients.strip():

        # Get recipe recommendations
        results = find_recipes(ingredients)

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