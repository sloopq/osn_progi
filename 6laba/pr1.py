from flask import Flask, render_template, request, make_response

answers = {
    "mommy": {"yes": 0, "no": 0, "not-sure": 0},
    "daddy": {"yes": 0, "no": 0, "not-sure": 0},
}
app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return "Страница не найдена"

@app.route("/")
@app.route("/index")
def show_questions():
    return render_template("questions.html")


@app.route("/results", methods = ["GET","POST"])
def process_information():
    if request.method == "GET":
        return render_template("answers1.html",
                               answers=answers)

    if request.method == "POST":
        if "voited" in request.cookies and \
                request.cookies["voited"] == "ok":
            return "Вы уже проголосовали"

        if "mommy" in request.form:
            if request.form["mommy"] == "yes":
                answers["mommy"]["yes"] += 1
            elif request.form["mommy"] == "no":
                answers["mommy"]["no"] += 1
            elif request.form["mommy"] == "not-sure":
                answers["mommy"]["not-sure"] += 1

        if "daddy" in request.form:
            if request.form["daddy"] == "yes":
                answers["daddy"]["yes"] += 1
            elif request.form["daddy"] == "no":
                answers["daddy"]["no"] += 1
            elif request.form["daddy"] == "not-sure":
                answers["daddy"]["not-sure"] += 1

        response = make_response(
                render_template("answers1.html", answers=answers)
        )

        response.set_cookie("voited","ok")

        return response

if __name__ == "__main__":
    app.run(host="127.0.0.1", port = 4321)