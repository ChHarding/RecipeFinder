import re

import html

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


/* Recipe title and match badge */
[data-testid="stExpander"] summary p {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    width: 100%;
    min-width: 0;
    margin: 0 !important;
    padding: 0 !important;
    transform: none !important;
}

/* Recipe name */
[data-testid="stExpander"] summary p strong {
    flex: 1;
    min-width: 0;
    overflow-wrap: anywhere;
    font-weight: 650;
}

/* Match percentage badge */
[data-testid="stExpander"] summary p > span:last-child {
    display: inline-flex;
    align-items: center;
    flex: 0 0 auto;
    margin-left: auto;
    padding: 4px 10px;
    background-color: #FFF0E8;
    color: #AE440C;
    border: 1px solid #FFD9C7;
    border-radius: 999px;
    white-space: nowrap;
    font-size: 12px;
    font-weight: 600;
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

/* Center navigation text */
div.st-key-nav_search button,
div.st-key-nav_favorites button {
    width: max-content !important;
    min-width: 0 !important;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
}

/* Top navigation tabs */
div.st-key-nav_search button,
div.st-key-nav_favorites button {
    position: relative;
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    color: #343541 !important;
    font-weight: 500;
    font-size: 16px !important;
    padding: 12px 0 !important;
}


/* Tab text */
div.st-key-nav_search button p,
div.st-key-nav_favorites button p {
    position: relative;
    width: fit-content;
    margin: 0 auto;
    font-size: 16px !important;
    line-height: 24px !important;
}


/* Center navigation text */
div.st-key-nav_search button,
div.st-key-nav_favorites button {
    width: max-content !important;
    min-width: 0 !important;
    margin: 0 auto !important;
    position: relative;
}

/* Active tab text */
div.st-key-nav_search button:disabled p,
div.st-key-nav_favorites button:disabled p {
    font-weight: 700 !important;
}

/* Active tab underline */
div.st-key-nav_search button:disabled,
div.st-key-nav_favorites button:disabled {
    border-bottom: 2px solid #FF5A00 !important;
}

/* Results page back arrow */
div.st-key-results_back button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    min-height: 36px;
    min-width: 36px;
}

/* Back arrow size */
div.st-key-results_back button p {
    font-size: 34px !important;
    line-height: 1 !important;
    font-weight: 400 !important;
    color: #202127 !important;
}

/* Favorite icon buttons */
div[class*="st-key-save_"] button,
div[class*="st-key-remove_"] button,
div[class*="st-key-favorite_remove_"] button {
    height: 40px;
    min-height: 40px;
    border: 1px solid #D1D5DB !important;
    border-radius: 6px !important;
    background: #FFFFFF !important;
    padding: 0 !important;
}

/* Filled orange heart for saved recipes */
div[class*="st-key-remove_"] button [data-testid="stIconMaterial"],
div[class*="st-key-favorite_remove_"] button [data-testid="stIconMaterial"] {
    font-variation-settings: 'FILL' 1 !important;
    color: #FF5A00 !important;
}

/* Center favorite icons */
div[class*="st-key-save_"] button,
div[class*="st-key-remove_"] button {
    justify-content: center !important;
    align-items: center !important;
}

/* Unsaved heart */
div[class*="st-key-save_"] button [data-testid="stIconMaterial"] {
    font-variation-settings: 'FILL' 0 !important;
    color: #343541 !important;
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

# Display ingredients as rounded chips
def display_ingredient_chips(ingredients, missing=False):
    color = "#FF5A00" if missing else "#374151"

    ingredient_text = ", ".join(
        html.escape(str(ingredient))
        for ingredient in ingredients
    )

    st.markdown(
        f'<div style="color:{color}; font-size:16px; line-height:1.6; margin-bottom:12px;">'
        f'{ingredient_text}</div>',
        unsafe_allow_html=True
    )

# Initialize favorite recipes
if "favorites" not in st.session_state:
    st.session_state.favorites = {}

# Store recipe search results
if "search_results" not in st.session_state:
    st.session_state.search_results = None

# Track the current page
if "page" not in st.session_state:
    st.session_state.page = "search"

# Return to search page and restore ingredients
def go_to_search():
    st.session_state.page = "search"

    for category, selected in st.session_state.get(
        "saved_ingredients", {}
    ).items():
        st.session_state[category] = selected.copy()

    st.session_state["manual_ingredients"] = (
        st.session_state.get("saved_manual_ingredients", "")
    )


# Ingredient options (shared across pages)
ingredients_options = {
    "🥩 Protein": [
        "chicken", "beef", "eggs", "shrimp"
    ],
    "🥦 Vegetables": [
        "tomato", "onion", "potato",
        "carrot", "broccoli", "lettuce"
    ],
    "🍚 Grains & Dairy": [
        "rice", "pasta", "bread",
        "milk", "cheese", "butter"
    ]
}

# Navigate to My Favorities
def go_to_favorites():
    if st.session_state.page == "search":
        st.session_state.saved_ingredients = {
            category: list(st.session_state.get(category, []))
            for category in ingredients_options
        }
        st.session_state.saved_manual_ingredients = (
            st.session_state.get("manual_ingredients", "")
        )
    st.session_state.page = "favorites"

# Page navigation
if st.session_state.page != "results":
    nav_search, nav_favorites = st.columns(2)

    with nav_search:
        st.button(
            "Find Recipes",
            key="nav_search",
            on_click=go_to_search,
            disabled=st.session_state.page == "search",
            use_container_width=True
        )

    with nav_favorites:
        st.button(
            "My Favorites",
            key="nav_favorites",
            on_click=go_to_favorites,
            disabled=st.session_state.page == "favorites",
            use_container_width=True
        )

    # Divider below navigation
    st.markdown(
        '<hr style="border:0; border-top:1px solid #E5E7EB; margin:0 0 16px 0; transform:translateY(-16px);">',
        unsafe_allow_html=True
    )


# Clear all selected ingredients
def clear_ingredients():
    for category in ingredients_options:
        st.session_state[category] = []

    st.session_state["manual_ingredients"] = ""

# Ingredient quick selection
if st.session_state.page == "search":

    st.subheader("What do you have?")
    st.write("Select ingredients below or enter your own")

   # Ingredient selection
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
        key="manual_ingredients"
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
        spacer, clear_col = st.columns([1, 1])

        with clear_col:
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

            # Save selected ingredients before switching pages
            st.session_state.saved_ingredients = {
                category: list(st.session_state.get(category, []))
                for category in ingredients_options
        }
            st.session_state.saved_manual_ingredients = st.session_state.get(
                "manual_ingredients", ""
            )
            # Go to the results page
            st.session_state.page = "results"
            st.rerun()

        else:
            st.warning("Please enter at least one ingredient.")


# Display saved search results 
results = st.session_state.search_results

if st.session_state.page == "results" and results is not None:

        # Results page header
        back_col, title_col, right_col = st.columns(
            [1, 2, 1],
            vertical_alignment="center"
        )

        with back_col:
            st.button(
                "‹",
                key="results_back",
                on_click=go_to_search,
                type="tertiary",
                help="Back to ingredients"
            )

        with title_col:
            st.markdown(
                '<div style="text-align:center; font-size:20px; font-weight:700;">Recipes</div>',
                unsafe_allow_html=True
            )

        # Divider below results header
        st.markdown(
            '<hr style="border:0; border-top:1px solid #E5E7EB; margin:8px 0 16px 0;">',
            unsafe_allow_html=True
        )

        
        corrections = st.session_state.get("search_corrections", [])

        if results:

            st.markdown(
                f'<div style="color:#16A36A; font-size:20px; font-weight:600;">'
                f'Found {len(results)} matching recipes!</div>',
                unsafe_allow_html=True
            )

        # Show ingredient corrections
        if corrections:
            for original, corrected in corrections:
                st.caption(
                    f"Ingredient recognized: {original} → {corrected}"
                )

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
                    f"**{recipe['name']}** :orange[{recipe['match']:.0f}% Match]",
                ):

                    # Required ingredients
                    st.write("**Required Ingredients:**")
                    display_ingredient_chips(recipe["ingredients"])

                    # Missing ingredients
                    st.write("**Missing Ingredients:**")

                    if recipe["missing"]:
                        display_ingredient_chips(recipe["missing"], missing=True)
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

                    # Right-align the favorite button
                    spacer, save_col = st.columns([7, 1.5])

                    with save_col:
                        if recipe_name in st.session_state.favorites:
                            if st.button(
                                "Saved",
                                icon=":material/favorite:",
                                key=f"remove_{recipe_name}",
                                help="Remove from favorites",
                                use_container_width=True
                            ):
                                del st.session_state.favorites[recipe_name]
                                st.rerun()
                        else:
                            if st.button(
                                "Save",
                                icon=":material/favorite_border:",
                                key=f"save_{recipe_name}",
                                help="Save recipe",
                                use_container_width=True
                            ):
                                st.session_state.favorites[recipe_name] = recipe.copy()
                                st.rerun()

        if not results:
            st.warning(
                "No matching recipes found."
            )

# My Favorites section
if st.session_state.page == "favorites":
    st.subheader(f"My Favorites ({len(st.session_state.favorites)})")

    if st.session_state.favorites:
        for recipe_name, recipe in st.session_state.favorites.items():

            with st.expander(f"**{recipe_name}**"):

                # Required ingredients
                st.write("**Required Ingredients:**")
                display_ingredient_chips(recipe["ingredients"])

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
                spacer, favorite_col = st.columns([7, 1.5])

                with favorite_col:
                    if st.button(
                        "Saved",
                        icon=":material/favorite:",
                        key=f"favorite_remove_{recipe_name}",
                        help="Remove from favorites",
                        use_container_width=True
                    ):
                        del st.session_state.favorites[recipe_name]
                        st.rerun()

    else:
        st.info("No favorite recipes yet. Save recipes to see them here.")