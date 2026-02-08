# Import Flask tools
# Flask = the web framework
# render_template = lets us use HTML files
# request = lets us read form data (checkboxes)
from flask import Flask, render_template, request

# Create the Flask app
# __name__ tells Flask where to look for files
app = Flask(__name__)


# -----------------------------
# SYMPTOM LIST (20 COMMON ONES)
# -----------------------------
# This list is sent to the website so users can
# click checkboxes instead of typing numbers

SYMPTOMS = [
    "Fever",
    "Cough",
    "Sore throat",
    "Runny or stuffy nose",
    "Sneezing",
    "Shortness of breath",
    "Chest pain",
    "Fatigue",
    "Headache",
    "Body aches",
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Stomach pain",
    "Loss of appetite",
    "Dizziness",
    "Rash",
    "Itchy or watery eyes",
    "Loss of taste or smell",
    "Chills"
]



# ILLNESS DATABASE (VERY SIMPLIFIED)

# Each illness has a list of symptoms
# The program compares user symptoms
# against these lists to find matches

ILLNESSES = {

    "Common Cold": [
        "Cough",
        "Sore throat",
        "Runny or stuffy nose",
        "Sneezing",
        "Fatigue",
        "Headache"
    ],

    "Flu": [
        "Fever",
        "Chills",
        "Body aches",
        "Fatigue",
        "Cough",
        "Headache"
    ],

    "Allergies": [
        "Sneezing",
        "Runny or stuffy nose",
        "Itchy or watery eyes",
        "Sore throat"
    ],

    "Stomach Bug": [
        "Nausea",
        "Vomiting",
        "Diarrhea",
        "Stomach pain",
        "Loss of appetite",
        "Fever"
    ],

    "COVID-like Illness": [
        "Fever",
        "Cough",
        "Fatigue",
        "Loss of taste or smell",
        "Shortness of breath",
        "Headache"
    ]
}



# HOME PAGE ROUTE

# This runs when someone visits "/"
# It loads index.html and sends the
# symptom list into the page

@app.route("/", methods=["GET"])
def home():

    # render_template loads the HTML file
    # symptoms=SYMPTOMS passes the list
    return render_template("index.html", symptoms=SYMPTOMS)



# RESULTS PAGE ROUTE

# This runs when the form is submitted
# It receives the checked symptoms

@app.route("/results", methods=["POST"])
def results():

    # request.form.getlist gets all checked boxes
    # Each checkbox sends its symptom text
    chosen = request.form.getlist("symptoms")


    # If user didn’t check anything
    if not chosen:
        return render_template(
            "results.html",
            chosen=[],
            results=[],
            best=[],
            message="No symptoms were selected. Go back and choose at least one."
        )


    # Store illness scores
    scored = []

    # Track best match
    best_score = 0
    best_list = []


    # Loop through every illness
    for illness_name, illness_symptoms in ILLNESSES.items():

        # Count matching symptoms
        match_count = 0

        # Compare user symptoms vs illness symptoms
        for s in chosen:
            if s in illness_symptoms:
                match_count += 1


        # Calculate percent match
        percent = (match_count / len(illness_symptoms)) * 100


        # Only store illnesses with at least 1 match
        if match_count > 0:
            scored.append({
                "name": illness_name,
                "match_count": match_count,
                "total": len(illness_symptoms),
                "percent": round(percent, 1),
            })


        # Track the best match (handles ties)
        if match_count > best_score:
            best_score = match_count
            best_list = [illness_name] if match_count != 0 else []

        elif match_count == best_score and match_count != 0:
            best_list.append(illness_name)


    # Sort illnesses from highest match → lowest
    scored.sort(
        key=lambda x: (x["match_count"], x["percent"]),
        reverse=True
    )


    # Send all results to the HTML page
    return render_template(
        "results.html",
        chosen=chosen,
        results=scored,
        best=best_list,
        message=""
    )



# RUN THE WEBSITE
# host=0.0.0.0 allows Codespaces
# to create a public forwarded link
# port=5000 is the web server port

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
