import re

import streamlit as st
from recipe_logic import find_recipes

st.markdown("""
<style>
div.stButton>button[kind="primary"] {
    background-color: #FF5A00;
    color: white;
    border: none;
    border-radius: 16px;
    font-weight: 600;
}


/* Recipe card header */
[data-testid="stExpander"] summary {
    position: relative;
}



/* Recipe card header */
[data-testid="stExpander"] summary {
    position: relative;
    padding-left: 16px !important;
    padding-right: 40px !important;
}

/* Title and arrow wrapper */
[data-testid="stExpander"] summary > span {
    display: flex;
    align-items: center;
    width: 100%;
    gap: 0 !important;
}

/* Move original arrow container to the right */
[data-testid="stExpander"] summary > span > span {
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    margin: 0 !important;
    padding: 0 !important;
}

/* Recipe title */
[data-testid="stExpander"] summary p {
    margin: 0 !important;
    padding: 0 !important;
    transform: none !important;
}

/* Recipe card content spacing */
[data-testid="stExpanderDetails"] {
    padding: 16px !important;
}

/* Reduce vertical spacing between elements */
[data-testid="stExpanderDetails"]
[data-testid="stVerticalBlock"] {
    gap: 0.5rem !important;
}

/* Remove default paragraph margins */
[data-testid="stExpanderDetails"] p {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    line-height: 1.5;
}

/* Reduce spacing between cooking steps */
[data-testid="stExpanderDetails"] 
[data-testid="stMarkdownContainer"] {
    margin-bottom: 0 !important;
}

/* Disabled primary button */
div.stButton>button[kind="primary"]:disabled {
    background-color: #F2F2F2;
    color: #A0A0A0;
    border: none;
    cursor: not-allowed;
    opacity: 1;
}

/* Keep disabled style on hover */
div.stButton>button[kind="primary"]:disabled:hover {
    background-color: #F2F2F2;
    color: #A0A0A0;
}

</style>
""", unsafe_allow_html=True)

# Display cooking instructions as numbered steps
def display_cooking_steps(instructions):
    steps = [
        step.strip()
        for step in re.split(r"(?<=[.!?])\s+", instructions.strip())
        if step.strip()
    ]

    for index, step in enumerate(steps, start=1):
        st.markdown(f"**{index:02d}.** {step}")

# Initialize favorite recipes
if "favorites" not in st.session_state:
    st.session_state.favorites = {}

# Store recipe search results
if "search_results" not in st.session_state:
    st.session_state.search_results = None

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
if st.button(
    "Find Recipes", 
    type="primary",
    disabled=len(all_ingredients) == 0
):

    if ingredients.strip():

        # Get recipe recommendations
        results, corrections = find_recipes(ingredients)
        st.session_state.search_results = results
        st.session_state.search_corrections = corrections

    else:
        st.warning("Please enter at least one ingredient.")

# Display saved search results 
results = st.session_state.search_results

if results is not None:
        corrections = st.session_state.get("search_corrections", [])

        # Show ingredient corrections
        if corrections:
            for original, corrected in corrections:
                st.info(f"Ingredient recognized: {original} → {corrected}")

        if results:

            st.success(f"Found {len(results)} matching recipes!")

            st.subheader("Recommended Recipes")

            # Fillter and sort  recipes recommandations
            filter_col, sort_col = st.columns(2)

            with filter_col:
                match_filter = st.selectbox(
                    "Filter by Match",
                    ["All Recipes", "≥ 50% or higher", "70% or higher", "90% or higher"],
                )

            with sort_col:
                sort_option = st.selectbox(
                    "Sort by",
                    [
                        "Highest Match",
                        "Lowest Match",
                        "Recipe Name (A-Z)"
                    ]
                )

            # Apply filter
            filtered_results = results.copy()

            if match_filter == "≥ 50% or higher":
                filtered_results = [
                    recipe for recipe in filtered_results
                    if recipe["match"] >= 50
                ]
            elif match_filter == "70% or higher":
                filtered_results = [
                    recipe for recipe in filtered_results
                    if recipe["match"] >= 70
                ]
            elif match_filter == "90% or higher":
                filtered_results = [
                    recipe for recipe in filtered_results
                    if recipe["match"] >= 90
                ]

            # Apply sorting
            if sort_option == "Highest Match":
                filtered_results.sort(
                    key=lambda recipe: recipe["match"],
                    reverse=True
                )

            elif sort_option == "Lowest Match":
                filtered_results.sort(
                    key=lambda recipe: recipe["match"],
                )
            elif sort_option == "Recipe Name (A-Z)":
                filtered_results.sort(
                    key=lambda recipe: recipe["name"].lower()
                )

            # Display recipe results
            for recipe in filtered_results:

                with st.expander(
                    f"{recipe['name']} - {recipe['match']:.0f}% Match"
                ):

                    # Required ingredients
                    st.write("**Required Ingredients:**")
                    st.write(", ".join(recipe["ingredients"]))

                    # Missing ingredients
                    st.write("**Missing Ingredients:**")

                    if recipe["missing"]:
                        st.write(", ".join(recipe["missing"]))
                    else:
                        st.write("None! You have all the ingredients.")

                    # Cooking instructions
                    st.write("**Cooking Instructions:**")

                    instructions = recipe["instructions"]

                    steps = [

                        step.strip()
                        for step in re.split(r"(?<=[.!?])\s+", instructions.strip())
                        if step.strip()
                    ]

                    for index, step in enumerate(steps, start=1):

                        st.markdown(f"**{index:02d}.** {step}")

                    # Save or remove favorite recipes
                    recipe_name = recipe["name"]

                    if recipe_name in st.session_state.favorites:
                        if st.button(
                             "❤️ Saved",
                             key=f"remove_{recipe_name}"
                      ):
                            del st.session_state.favorites[recipe_name]
                            st.rerun()

                    else:
                        if st.button(
                            "🤍 Save",
                            key=f"save_{recipe_name}"
                        ):
                            st.session_state.favorites[recipe_name] = recipe.copy()
                            st.rerun()


        else:
            st.warning(
                "No recipes found with at least 40% ingredient match."
            )

# My Favorites section
st.divider()
st.subheader(f"❤️ My Favorites ({len(st.session_state.favorites)})")

if st.session_state.favorites:
    for recipe_name, recipe in st.session_state.favorites.items():

        with st.expander(recipe_name):

            # Required ingredients
            st.write("**Required Ingredients:**")
            st.write(", ".join(recipe["ingredients"]))

            # Cooking instructions
            st.write("**Cooking Instructions:**")

            instructions = recipe["instructions"]
            # Split instructions into steps based on numbering or new lines
            steps = [
                step.strip()
                for step in re.split(r"(?<=[.!?])\s+", instructions.strip())
                if step.strip()
            ]

            for index, step in enumerate(steps, start=1):
                st.markdown(f"**{index:02d}.** {step}")

            # Remove from favorites
            if st.button(
                "❤️ Remove from Favorites",
                key=f"favorite_remove_{recipe_name}"
            ):
                del st.session_state.favorites[recipe_name]
                st.rerun()
else:
    st.info("No favorite recipes yet. Save recipes to see them here.")