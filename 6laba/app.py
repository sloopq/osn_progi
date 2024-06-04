from flask import Flask, render_template, request, make_response, redirect, url_for
import json
import os

app = Flask(__name__)


RESULTS_FILE = "results.json"

def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "mommy": {"yes": 0, "no": 0, "not-sure": 0},
            "daddy": {"yes": 0, "no": 0, "not-sure": 0},
        }

def save_results(answers):
    with open(RESULTS_FILE, "w") as f:
        json.dump(answers, f)

answers = load_results()

@app.route("/")
@app.route("/questions")
def show_questions():
    if request.cookies.get("voted") == "ok":
        return render_template("already_voted.html")
    return render_template("questions.html")

@app.route("/results", methods=["GET", "POST"])
def process_information():
    if request.method == "GET":
        return render_template("answer.html", answers=answers)

    if request.method == "POST":
        if request.cookies.get("voted") == "ok":
            return "Вы уже проголосовали"

        if "mommy" in request.form:
            answers["mommy"][request.form["mommy"]] += 1

        if "daddy" in request.form:
            answers["daddy"][request.form["daddy"]] += 1

        save_results(answers)

        response = make_response(render_template("answer.html", answers=answers))
        response.set_cookie("voted", "ok")

        return response

@app.route("/change_answers")
def change_answers():
    global answers
    answers = {
        "mommy": {"yes": 0, "no": 0, "not-sure": 0},
        "daddy": {"yes": 0, "no": 0, "not-sure": 0},
    }
    save_results(answers)
    response = make_response(redirect(url_for("show_questions")))
    response.set_cookie("voted", "")
    return response

@app.route("/view_results")
def view_results():
    answers = load_results()
    return render_template("view_results.html", answers=answers)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4321)
