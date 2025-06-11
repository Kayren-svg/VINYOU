import streamlit as st
import pandas as pd
import os

# ------------------------ WINE DATA ------------------------ #
wines_data = [
    {"name": "Château Margaux", "type": "Red", "profile": ["tannic", "full-bodied", "complex"], "region": "Bordeaux"},
    {"name": "Château Latour", "type": "Red", "profile": ["powerful", "structured", "long finish"], "region": "Bordeaux"},
    {"name": "Château d'Yquem", "type": "White Sweet", "profile": ["sweet", "rich", "honeyed"], "region": "Sauternes"},
    {"name": "Domaine de la Romanée-Conti", "type": "Red", "profile": ["elegant", "floral", "earthy"], "region": "Bourgogne"},
    {"name": "Clos de Vougeot", "type": "Red", "profile": ["tannic", "spicy", "complex"], "region": "Bourgogne"},
    {"name": "Meursault", "type": "White", "profile": ["buttery", "nutty", "round"], "region": "Bourgogne"},
    {"name": "Chablis Grand Cru Les Clos", "type": "White", "profile": ["mineral", "dry", "citrus"], "region": "Bourgogne"},
    {"name": "Côte-Rôtie", "type": "Red", "profile": ["spicy", "meaty", "tannic"], "region": "Rhône"},
    {"name": "Hermitage Blanc", "type": "White", "profile": ["rich", "floral", "almond"], "region": "Rhône"},
    {"name": "Châteauneuf-du-Pape", "type": "Red", "profile": ["spicy", "fruity", "full-bodied"], "region": "Rhône"},
    {"name": "Saint-Émilion Grand Cru", "type": "Red", "profile": ["smooth", "fruity", "velvety"], "region": "Bordeaux"},
    {"name": "Pommard", "type": "Red", "profile": ["structured", "earthy", "cherry"], "region": "Bourgogne"},
    {"name": "Sancerre Blanc", "type": "White", "profile": ["dry", "flinty", "citrus"], "region": "Loire"},
    {"name": "Pouilly-Fumé", "type": "White", "profile": ["smoky", "dry", "mineral"], "region": "Loire"},
    {"name": "Cornas", "type": "Red", "profile": ["peppery", "dense", "tannic"], "region": "Rhône"},
]
wines_df = pd.DataFrame(wines_data)

# ------------------------ TASTE PREFERENCES ------------------------ #
preferences = [
    "fruity", "dry", "tannic", "floral", "spicy", "mineral", "light",
    "sweet", "full-bodied", "fresh", "smoky", "brut", "salty", "vegetal",
    "powerful", "acidic", "sugary", "citrus", "earthy", "complex"
]

# ------------------------ STREAMLIT UI ------------------------ #
st.set_page_config(page_title="VINYOU – Wine Quiz", page_icon="🍷")
st.title("🍷 VINYOU – Discover Your Perfect French Wine")

st.markdown("Answer a few questions and we'll match you with three of the finest French wines 🍇.")

name = st.text_input("What is your name?")
gender = st.radio("What is your gender?", ["Female", "Male", "Other"])

st.markdown("### What tastes do you enjoy in wine?")
selected_prefs = st.multiselect("Select your preferred taste profiles:", preferences)

wine_type = st.radio("What type of wine do you prefer?", ["Red", "White", "Rosé", "White Sweet", "Any"])

# ------------------------ MATCHING FUNCTION ------------------------ #
def match_score(wine_profiles, user_prefs):
    return sum(p in user_prefs for p in wine_profiles)

# ------------------------ ACTION ------------------------ #
if st.button("🎯 Submit and get matched"):
    if not name or not gender or not selected_prefs:
        st.warning("Please complete all fields (name, gender, taste preferences).")
    else:
        # Filter wines by preferred type
        filtered_df = wines_df if wine_type == "Any" else wines_df[wines_df["type"] == wine_type]
        filtered_df["score"] = filtered_df["profile"].apply(lambda x: match_score(x, selected_prefs))
        top_matches = filtered_df.sort_values(by="score", ascending=False).head(3)

        wine_names = top_matches["name"].tolist()

        # Record response
        entry = {
            "name": name.strip().lower(),
            "gender": gender,
            "wine_type_preference": wine_type,
            "preferences": ", ".join(selected_prefs),
            "wine_1": wine_names[0] if len(wine_names) > 0 else "",
            "wine_2": wine_names[1] if len(wine_names) > 1 else "",
            "wine_3": wine_names[2] if len(wine_names) > 2 else "",
        }

        filename = "responses.csv"
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            df = df[df["name"] != entry["name"]]  # Remove previous entry
            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        else:
            df = pd.DataFrame([entry])
        df.to_csv(filename, index=False)

        # Confirmation message
        st.success("✅ Your answers have been saved! Thank you for participating 🍷")

        # GIF (funny/fancy wine toast)
        st.markdown("![cheers](https://media.giphy.com/media/3o7btMCltyDvSgF92E/giphy.gif)")

