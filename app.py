from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from dataset_loader import load_dataset
import os

app = Flask(__name__)
CORS(app)

df = load_dataset(
    "42_cases_under_crime_against_women.csv"
)

df_arrests = load_dataset(
    "43_Arrests_under_crime_against_women.csv"
)

df_property = load_dataset(
    "10_Property_stolen_and_recovered.csv"
)


df_rape_victims = load_dataset(
    "20_Victims_of_rape.csv"
)

df_police_complaints = load_dataset(
    "25_Complaints_against_police.csv"
)

df_violent_trials = load_dataset(
    "28_Trial_of_violent_crimes_by_courts.csv"
)

df_trial_period = load_dataset(
    "29_Period_of_trials_by_courts.csv"
)

df_auto_theft = load_dataset(
    "30_Auto_theft.csv"
)

df_serious_fraud = load_dataset(
    "31_Serious_fraud.csv"
)

df_murder_victims = load_dataset(
    "32_Murder_victim_age_sex.csv"
)

df_non_murder_victims = load_dataset(
    "33_CH_not_murder_victim_age_sex.csv"
)

df_human_rights = load_dataset(
    "35_Human_rights_violation_by_police.csv"
)

df_police_housing = load_dataset(
    "36_Police_housing.csv"
)

df_police_housing = load_dataset(
    "36_Police_housing.csv"
)

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

@app.route("/arrests-trend")
def arrests_trend():

    yearly = (
        df_arrests.groupby("Year")["Persons_Arrested"]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "arrests": int(row["Persons_Arrested"])
        })

    return jsonify(data)


@app.route("/property-trend")
def property_trend():

    yearly = (
        df_property.groupby("Year")[
            ["Cases_Property_Stolen", "Cases_Property_Recovered"]
        ]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "stolen": int(row["Cases_Property_Stolen"]),
            "recovered": int(row["Cases_Property_Recovered"])
        })

    return jsonify(data)

@app.route("/rape-victims-trend")
def rape_victims_trend():

    yearly = (
        df_rape_victims[
            df_rape_victims["Subgroup"] == "Total Rape Victims"
        ]
        .groupby("Year")["Victims_of_Rape_Total"]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "victims": int(row["Victims_of_Rape_Total"])
        })

    return jsonify(data)

@app.route("/police-complaints-trend")
def police_complaints_trend():

    yearly = (
        df_police_complaints.groupby("Year")[
            "CPA_-_Complaints_Received/Alleged"
        ]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "complaints": int(row["CPA_-_Complaints_Received/Alleged"])
        })

    return jsonify(data)

@app.route("/violent-trials-trend")
def violent_trials_trend():

    yearly = (
        df_violent_trials.groupby("Year")[
            "Trial_of_Violent_Crimes_by_Courts_Total"
        ]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "trials": int(row["Trial_of_Violent_Crimes_by_Courts_Total"])
        })

    return jsonify(data)

@app.route("/trial-period-trend")
def trial_period_trend():

    yearly = (
        df_trial_period.groupby("Year")[
            [
                "PT_Less_than_6_Months",
                "PT_6_12_Months",
                "PT_1_3_Years",
                "PT_3_5_Years",
                "PT_5_10_Years",
                "PT_Over_10_Years"
            ]
        ]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "less_than_6_months": int(row["PT_Less_than_6_Months"]),
            "six_to_12_months": int(row["PT_6_12_Months"]),
            "one_to_3_years": int(row["PT_1_3_Years"]),
            "three_to_5_years": int(row["PT_3_5_Years"]),
            "five_to_10_years": int(row["PT_5_10_Years"]),
            "over_10_years": int(row["PT_Over_10_Years"])
        })

    return jsonify(data)

@app.route("/auto-theft-trend")
def auto_theft_trend():

    yearly = (
        df_auto_theft.groupby("Year")[
            [
                "Auto_Theft_Stolen",
                "Auto_Theft_Recovered",
                "Auto_Theft_Coordinated/Traced"
            ]
        ]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "stolen": int(row["Auto_Theft_Stolen"]),
            "recovered": int(row["Auto_Theft_Recovered"]),
            "traced": int(row["Auto_Theft_Coordinated/Traced"])
        })

    return jsonify(data)


@app.route("/serious-fraud-trend")
def serious_fraud_trend():

    yearly = (
        df_serious_fraud.groupby("Year")[
            [
                "Loss_of_Property_1_10_Crores",
                "Loss_of_Property_10_25_Crores",
                "Loss_of_Property_25_50_Crores",
                "Loss_of_Property_50_100_Crores",
                "Loss_of_Property_Above_100_Crores"
            ]
        ]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "one_to_10_crores": int(row["Loss_of_Property_1_10_Crores"]),
            "ten_to_25_crores": int(row["Loss_of_Property_10_25_Crores"]),
            "twentyfive_to_50_crores": int(row["Loss_of_Property_25_50_Crores"]),
            "fifty_to_100_crores": int(row["Loss_of_Property_50_100_Crores"]),
            "above_100_crores": int(row["Loss_of_Property_Above_100_Crores"])
        })

    return jsonify(data)


@app.route("/murder-victim-trend")
def murder_victim_trend():

    yearly = (
        df_murder_victims.groupby(["Year", "Group_Name"])["Victims_Total"]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "group": str(row["Group_Name"]),
            "victims": int(row["Victims_Total"])
        })

    return jsonify(data)

@app.route("/non-murder-victim-trend")
def non_murder_victim_trend():

    yearly = (
        df_non_murder_victims.groupby(["Year", "Sub_Group_Name"])["Victims_Total"]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "group": str(row["Sub_Group_Name"]),
            "victims": int(row["Victims_Total"])
        })

    return jsonify(data)


@app.route("/human-rights-trend")
def human_rights_trend():

    yearly = (
        df_human_rights.groupby("Year")[
            [
                "Cases_Registered_under_Human_Rights_Violations",
                "Policemen_Chargesheeted",
                "Policemen_Convicted"
            ]
        ]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "cases_registered": int(row["Cases_Registered_under_Human_Rights_Violations"]),
            "chargesheeted": int(row["Policemen_Chargesheeted"]),
            "convicted": int(row["Policemen_Convicted"])
        })

    return jsonify(data)

@app.route("/police-housing-trend")
def police_housing_trend():

    yearly = (
        df_police_housing.groupby("Year")[
            [
                "PH_Houses_Provided_by_Department",
                "PH_Houses_provided_on_LeaseRentGPRA",
                "PH_Sanctioned_Strength"
            ]
        ]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():
        data.append({
            "year": str(int(row["Year"])),
            "houses_provided": int(row["PH_Houses_Provided_by_Department"]),
            "houses_on_lease": int(row["PH_Houses_provided_on_LeaseRentGPRA"]),
            "sanctioned_strength": int(row["PH_Sanctioned_Strength"])
        })

    return jsonify(data)

@app.route("/kidnapping-purpose-trend")
def kidnapping_purpose_trend():

    yearly = (
        df_kidnapping_purpose.groupby(
            ["Year", "Group_Name"]
        )["K_A_Grand_Total"]
        .sum()
        .reset_index()
    )

    data = []

    for _, row in yearly.iterrows():

        data.append({
            "year": str(int(row["Year"])),
            "purpose": str(row["Group_Name"]),
            "cases": int(row["K_A_Grand_Total"])
        })

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)