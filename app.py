from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from api import (
    AVAILABLE_SOURCES,
    add_ids,
    remove_duplicate,
    apply_filters,
    score_and_rank_jobs
)

app = Flask(__name__)
CORS(app)

@app.route("/search-jobs", methods=["POST"])
def search_jobs():

    data = request.json

    query = data.get("query", "software engineer")

    expected_salary = data.get("expected_salary")

    if expected_salary:
        expected_salary = float(expected_salary)
    else:
        expected_salary = None

    location = data.get("location", "INDIA KOLKATA")
    results_wanted = int(data.get("results_wanted", 20))
    country = data.get("country", "India")
    selected_sources = data.get(
        "selected_sources",
        []
    )

    if not selected_sources:
        selected_sources = list(
            AVAILABLE_SOURCES.keys()
        )

    valid_sources = []

    for source in selected_sources:

        if source in AVAILABLE_SOURCES:
            valid_sources.append(source)

    selected_sources = valid_sources

    result = []

    for source in selected_sources:

        name, fetch_func = AVAILABLE_SOURCES[source]

        try:
            if source in [
              
                "indeed",
                "linkedin",
                "zip_recruiter",
                "glassdoor",
                "google",
                "naukri",
                "bayt",
                "bdjobs"


            
            ]:

                jobs = fetch_func(
                    query,
                    location,
                    results_wanted,
                    country
                )

            else:
                jobs = fetch_func()

            result.extend(jobs)

        except Exception as e:
            print(f"Error fetching from {name}: {e}")

    result = add_ids(result)
    result = remove_duplicate(result)

    result = apply_filters(
        result,
        query=query,
        expected_salary=expected_salary,
        allowed_sources=None
    )

    result = score_and_rank_jobs(
        result,
        query=query,
        expected_salary=expected_salary,
        min_score=30,
        limit=50
    )

    with open("result.json", "w") as f:
        json.dump(result, f, indent=4)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
    