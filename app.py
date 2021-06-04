from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] ='password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# questions = satisfaction_survey.questions

@app.route('/')
def choose_survey():
    return render_template("choose_survey.html", surveys = surveys)

@app.route('/', methods = ['POST'])
def survey_session():
    survey_name = request.form['survey']
    survey = surveys[survey_name]
    session['survey'] = survey_name

    return render_template("homepage.html", survey = survey)

# @app.route('/homepage')
# def show_homepage():
    
#     # title = survey.title
#     # instructions = survey.instructions

#     return render_template("homepage.html", title = title, instructions = instructions)

@app.route('/start')
def start():
    session['responses'] = []
    return redirect("/questions/0")

@app.route('/questions/<int:q_number>')
def show_questions(q_number):
    responses = session.get('responses')
    survey_name = session['survey']
    questions = surveys[survey_name].questions  

    if q_number >= len(questions):
        return redirect('/')

    if len(responses) != q_number:
        flash("You can't access questions out of order!")
        return redirect(f"/questions/{len(responses)}")

    if len(responses) == len(questions):
        return redirect("/complete")

    return render_template("questions.html", allow_text = questions[q_number].allow_text, q_number = q_number, question = questions[q_number].question, choices = questions[q_number].choices)


@app.route("/answer", methods = ["POST"])
def add_answer():
    answer = request.form['answer']
    comment = request.form.get('text', '')
    
    survey_name = session['survey']
    questions = surveys[survey_name].questions

    responses = session['responses']
    responses.append({"answer": answer, "comment": comment})
    session['responses'] = responses

    

    if len(responses) == len(questions):
        return redirect("/complete")
    if len(responses) < len(questions):
       return redirect(f"/questions/{len(responses)}") 

@app.route("/complete")
def completed_survery():
    survey_name = session['survey']
    responses = session.get('responses')
    return render_template("complete.html", survey=surveys[survey_name], responses=responses)
    