# RecipeFinder

RecipeFinder is a Python application that recommends recipes based on ingredients users already have.

The goal of this project is to help users find recipes using available ingredients and reduce food waste.

## Features

- Search for recipes by entering available ingredients.
- Calculate ingredient match percentages.
- Sort recommended recipes from highest to lowest match.
- Display required and missing ingredients.
- Show cooking instructions for each recipe.
- Automatically correct common ingredient spelling mistakes.
- Remove duplicate ingredients from user input.
- Provide feedback when no ingredients are entered or no recipes match.
- Use a simple web interface built with Streamlit.

## Technologies Used

- Python
- Streamlit
- Pandas
- RapidFuzz
- CSV

## Project Structure

- `app.py` - Streamlit web interface.
- `recipe_logic.py` - Recipe matching and spelling correction logic.
- `recipes.csv` - Recipe dataset.
- `main.py` - Original command-line version.
- `README.md` - Project documentation.

## How to Run

1. Install the required Python libraries:

   ```bash
   pip install streamlit pandas rapidfuzz
      ```

2. Run the Streamlit application:

   ```bash
   python3 -m streamlit run app.py
   ```

3. Open the local URL displayed in the terminal.

4. Enter ingredients separated by commas.

5. Click "Find Recipes" to view recommendations.

## Example

Input:

chiken, tomat

The application automatically corrects the spelling:

- chiken → chicken
- tomat → tomato

It then displays matching recipes with match percentages, missing ingredients, and cooking instructions.

## Current Progress

The application currently includes a working Streamlit interface, recipe matching, spelling correction, duplicate ingredient handling, and basic input validation.

## Future Improvements

- Expand the recipe dataset.
- Improve ingredient matching accuracy.
- Continue improving the user interface.
- Add more testing for different ingredient combinations.