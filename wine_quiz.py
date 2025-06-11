
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
    {"name": "Château Margaux", "type": "Red", "profile": ["tannic", "full-bodied", "complex"], "region": "Bordeaux"},
    {"name": "Meursault", "type": "White", "profile": ["buttery", "nutty", "round"], "region": "Bourgogne"},
    {"name": "Château d'Yquem", "type": "White Sweet", "profile": ["sweet", "rich", "honeyed"], "region": "Sauternes"}
]
wines_df = pd.DataFrame(wines)
preferences = ["fruity", "dry", "tannic", "sweet", "complex"]

st.title("🍷 VINYOU – Wine Quiz")
name = st.text_input("Your name:")
gender = st.radio("Gender:", ["Female", "Male", "Other"])
selected_prefs = st.multiselect("Taste preferences:", preferences)
wine_type = st.radio("Preferred wine type:", ["Red", "White", "Rosé", "White Sweet", "Any"])

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
