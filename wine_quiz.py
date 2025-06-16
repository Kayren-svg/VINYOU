
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Connexion à Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)
sheet = client.open("vinyou_responses").sheet1

def save_to_google_sheets(entry):
    sheet.append_row([
        entry["name"],
        entry["gender"],
        entry["wine_type_preference"],
        entry["preferences"],
        entry["wine_1"],
        entry["wine_2"],
        entry["wine_3"],
    ])

# Interface Streamlit simplifiée
wines = [
    {"name": "Chablis 1er Cru Montée de Tonnerre 2020", "type": "White", "profile": ["dry", "fruity", "complex"], "region": "Bourgogne"},
    {"name": "Château La Nerthe 2018", "type": "Red", "profile": ["tannic", "complex", "dry"], "region": "Châteauneuf-du-Pape"},
    {"name": "Domaine Zind-Humbrecht Riesling 2019", "type": "White", "profile": ["fruity", "dry", "complex"], "region": "Alsace"},
    {"name": "Bandol Domaine Tempier 2020", "type": "Rosé", "profile": ["fruity", "dry", "complex"], "region": "Provence"},
    {"name": "Château Haut-Bailly 2016", "type": "Red", "profile": ["tannic", "complex", "dry"], "region": "Pessac-Léognan"},
    {"name": "Pouilly-Fumé Didier Dagueneau 2021", "type": "White", "profile": ["dry", "fruity"], "region": "Loire"},
    {"name": "Côte-Rôtie La Turque 2017", "type": "Red", "profile": ["tannic", "complex", "dry"], "region": "Rhône"},
    {"name": "Mâcon-Villages Joseph Drouhin 2022", "type": "White", "profile": ["fruity", "dry"], "region": "Bourgogne"},
    {"name": "Clos de Tart Grand Cru 2015", "type": "Red", "profile": ["tannic", "complex"], "region": "Bourgogne"},
    {"name": "Gewurztraminer Vendanges Tardives 2018", "type": "White", "profile": ["sweet", "fruity", "complex"], "region": "Alsace"},
    {"name": "Tavel Domaine de la Mordorée 2021", "type": "Rosé", "profile": ["fruity", "dry"], "region": "Rhône"},
    {"name": "Château d’Yquem 2005", "type": "White Sweet", "profile": ["sweet", "complex"], "region": "Sauternes"},
    {"name": "Chinon Les Picasses 2020", "type": "Red", "profile": ["tannic", "dry", "fruity"], "region": "Loire"},
    {"name": "Picpoul de Pinet 2022", "type": "White", "profile": ["dry", "fruity"], "region": "Languedoc"},
    {"name": "Cornas Vieilles Vignes 2017", "type": "Red", "profile": ["tannic", "complex", "dry"], "region": "Rhône"}
]
wines_df = pd.DataFrame(wines)
preferences = ["fruity", "dry", "tannic", "sweet", "complex"]

st.title("🍷 VINYOU – Wine Quiz")
name = st.text_input("Your name:")
gender = st.radio("Gender:", ["Female", "Male", "Other"])
selected_prefs = st.multiselect("Taste preferences:", preferences)
wine_type = st.radio("Preferred wine type:", ["Red", "White", "Rosé", "Sweet", "Any"])

def match_score(wine_profiles, user_prefs):
    return sum(p in user_prefs for p in wine_profiles)

if st.button("Submit"):
    if not name or not gender or not selected_prefs:
        st.warning("Please complete all fields.")
    else:
        filtered = wines_df if wine_type == "Any" else wines_df[wines_df["type"] == wine_type]
        filtered["score"] = filtered["profile"].apply(lambda x: match_score(x, selected_prefs))
        top = filtered.sort_values(by="score", ascending=False).head(3)
        wines_list = top["name"].tolist()
        entry = {
            "name": name.strip().lower(),
            "gender": gender,
            "wine_type_preference": wine_type,
            "preferences": ", ".join(selected_prefs),
            "wine_1": wines_list[0] if len(wines_list) > 0 else "",
            "wine_2": wines_list[1] if len(wines_list) > 1 else "",
            "wine_3": wines_list[2] if len(wines_list) > 2 else "",
        }
        save_to_google_sheets(entry)
        st.success("✅ Your response was saved successfully!")
