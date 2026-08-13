from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load dataset
DATASET_PATH = "../crimeverse-data/dataset/cleaned/crime_cleaned.csv"

df = pd.read_csv(DATASET_PATH)


@app.route("/")
def home():
    return "CrimeVerse Backend Running!"


@app.route("/summary")
def summary():

    total_cases = int(df["Cases_Reported"].sum())

    top_state = (
        df.groupby("Area_Name")["Cases_Reported"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    top_crime = (
        df.groupby("Sub_Group_Name")["Cases_Reported"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    return jsonify({
        "total_cases": total_cases,
        "top_state": top_state,
        "top_crime": top_crime
    })


@app.route("/trend")
def trend():

    yearly = (
        df.groupby("Year")["Cases_Reported"]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():

        data.append({
            "month": str(int(row["Year"])),
            "incidents": int(row["Cases_Reported"])
        })

    return jsonify(data)


@app.route("/crime-types")
def crime_types():

    crimes = (
        df.groupby("Sub_Group_Name")["Cases_Reported"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    data = []

    for _, row in crimes.iterrows():

        data.append({
            "name": row["Sub_Group_Name"],
            "value": int(row["Cases_Reported"])
        })

    return jsonify(data)


@app.route("/recent-incidents")
def recent_incidents():

    top = (
        df.groupby(
            ["Sub_Group_Name", "Area_Name"]
        )["Cases_Reported"]
        .sum()
        .sort_values(ascending=False)
        .head(4)
        .reset_index()
    )

    incidents = []

    for i, row in top.iterrows():

        incidents.append({
            "id": f"CV-2026-{8400 + i}",
            "crime": row["Sub_Group_Name"],
            "district": row["Area_Name"],
            "cases": int(row["Cases_Reported"])
        })

    return jsonify(incidents)


@app.route("/ai-insight")
def ai_insight():

    top_state = (
        df.groupby("Area_Name")["Cases_Reported"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    top_crime = (
        df.groupby("Sub_Group_Name")["Cases_Reported"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    total_cases = int(
        df["Cases_Reported"].sum()
    )

    return jsonify({
        "title": "AI Intelligence Summary",
        "summary": (
            f"{top_state} has reported the highest number "
            f"of crime cases. The most common crime category "
            f"is '{top_crime}'. A total of "
            f"{total_cases:,} crime cases are available "
            f"for analysis."
        ),
        "confidence": 96
    })


if __name__ == "__main__":
    app.run(debug=True)