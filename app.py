from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] ='password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
questions = satisfaction_survey.questions

@app.route('/')
def show_homepage():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    responses.clear()

    return render_template("homepage.html", title = title, instructions = instructions)

@app.route('/questions/<int:q_number>')
def show_questions(q_number):
    if q_number >= len(questions):
        return redirect('/')

    if len(responses) != q_number:
        flash("You can't access questions out of order!")
        return redirect(f"/questions/{len(responses)}")

    if len(responses) == len(questions):
        return redirect("/complete")

    return render_template("questions.html", q_number = q_number, question = questions[q_number].question, choices = questions[q_number].choices)


@app.route("/answer", methods = ["POST"])
def add_answer():
    answer = request.form['answer']
    responses.append(answer)

    if len(responses) == len(questions):
        return redirect("/complete")
    if len(responses) < len(questions):
       return redirect(f"/questions/{len(responses)}") 

@app.route("/complete")
def completed_survery():
    return render_template("complete.html", responses=responses)
    