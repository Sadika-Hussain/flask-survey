from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pancakes'

# Disable intercepting redirects by the debug toolbar
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Set up the Flask-DebugToolbar extension
debug_toolbar = DebugToolbarExtension(app)

# List to store responses from the survey
responses = []

def get_total_questions():
    """Return the total number of questions in the survey."""
    return len(satisfaction_survey.questions)

def get_total_responses():
    """Return the total number of responses recorded."""
    return len(responses)

@app.route('/')
def home():
    """
    Render the home page with survey instructions.
    """
    return render_template('home.html', satisfaction = satisfaction_survey)

@app.route('/questions/<int:question_id>')
def questions(question_id):
    """
    - Render the question page based on the question ID.
    - Redirect to the thank you page if all questions have been answered.
    - Redirect to the next unanswered question if user skips by entering question number in URL.
    """
    total_questions = get_total_questions()
    total_responses = get_total_responses()

    # Redirect to thank you page if all questions have been answered
    if total_responses == total_questions:
        return redirect('/thankyou')
    
    # Flash a message and redirect if the current question is unanswered
    if question_id != total_responses:
        flash('Please answer this question first')
        return redirect(f'{total_responses}') 
    
    # Get the current question from the survey to render on page
    question = satisfaction_survey.questions[question_id]
    return render_template('question.html', question=question, question_id=question_id)

@app.route('/answer/<int:question_id>', methods=['POST'])
def answer(question_id):
    """ Handle answer submission. """

    # Get the chosen answer from the form submission and append it to the responses list 
    choice = request.form.get('choice')
    responses.append(choice)

    # Redirect to next question
    return redirect(f'/questions/{question_id}')

@app.route('/thankyou')
def thankyou():
    """
    Render the thank you page if all questions have been answered.
    
    """
    total_questions = get_total_questions()
    total_responses = get_total_responses()

    # Redirect to the next unanswered question if all questions have not been answered.
    if total_responses != total_questions:
        flash('Please answer this question first')
        return redirect(f'/questions/{total_responses}')

    return render_template('thankyou.html')




