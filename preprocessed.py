import pandas as pd
from pathlib import Path

BASE_DIR = Path(".")
OUTPUT_DIR = BASE_DIR / "processed"
OUTPUT_DIR.mkdir(exist_ok=True)

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df

# Load Data
batting = pd.read_csv("./cricket_data/batting_records.csv")
matches = pd.read_csv("./cricket_data/matches.csv")
players = pd.read_csv("./cricket_data/players.csv")
teams = pd.read_csv("./cricket_data/teams.csv")
venues = pd.read_csv("./cricket_data/venues.csv")
india_venues = pd.read_csv("./cricket_data/india_venues.csv")
tournaments = pd.read_csv("./cricket_data/tournaments.csv")

# Clean Column Names
batting = clean_columns(batting)
matches = clean_columns(matches)
players = clean_columns(players)
teams = clean_columns(teams)
venues = clean_columns(venues)
india_venues = clean_columns(india_venues)
tournaments = clean_columns(tournaments)

# Batting Records Processing
batting.rename(columns={"stat_value": "value"}, inplace=True)

batting["value"] = pd.to_numeric(batting["value"], errors="coerce")
batting.dropna(subset=["player", "value"], inplace=True)

# Matches Processing
if "year" in matches.columns:
    matches["year"] = pd.to_numeric(matches["year"], errors="coerce")

matches.dropna(subset=["winner"], inplace=True)

# Teams Processing
for col in ["matches", "wins"]:
    if col in teams.columns:
        teams[col] = pd.to_numeric(teams[col], errors="coerce")

if {"matches", "wins"}.issubset(teams.columns):
    teams["win_percentage"] = (teams["wins"] / teams["matches"]) * 100

# India Venues Processing
for col in [
    "latitude",
    "longitude",
    "matches_played",
    "matches_won",
    "win_percentage",
    "avg_runs_scored",
]:
    if col in india_venues.columns:
        india_venues[col] = pd.to_numeric(india_venues[col], errors="coerce")

# Save Cleaned Files
batting.to_csv(OUTPUT_DIR / "batting_records_clean.csv", index=False)
matches.to_csv(OUTPUT_DIR / "matches_clean.csv", index=False)
players.to_csv(OUTPUT_DIR / "players_clean.csv", index=False)
teams.to_csv(OUTPUT_DIR / "teams_clean.csv", index=False)
venues.to_csv(OUTPUT_DIR / "venues_clean.csv", index=False)
india_venues.to_csv(OUTPUT_DIR / "india_venues_clean.csv", index=False)
tournaments.to_csv(OUTPUT_DIR / "tournaments_clean.csv", index=False)

print("Preprocessing complete.")
print(f"Cleaned files saved in: {OUTPUT_DIR.resolve()}")
