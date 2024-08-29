from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pancakesss'

# Disable intercepting redirects by the debug toolbar
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Set up the Flask-DebugToolbar extension
debug_toolbar = DebugToolbarExtension(app)

@app.route('/')
def start_page():
    """
    Render the home page with survey instructions.
    """
    return render_template('start_page.html', satisfaction = survey)

@app.route('/questions/<int:question_id>')
def questions(question_id):
    """
    Render the question page based on the question ID, with necessary redirects for skipped or completed questions.
    """
    responses = session.get('responses')

    # Redirect to start page if user tries to access a question without starting the survey    
    if responses is None:
        return redirect('/')

    # Redirect to thank you page if all questions have been answered
    if len(responses) == len(survey.questions):
        return redirect('/thankyou')
    
    # Redirect to the correct question if the user tries to skip ahead
    if question_id != len(responses):
        flash('Please answer this question first')
        return redirect(f'{len(responses)}') 
    
    # Get the current question from the survey to render on page
    question = survey.questions[question_id]
    return render_template('question.html', question=question, question_id=question_id)

@app.route('/answer/<int:question_id>', methods=['POST'])
def answer(question_id):
    """ Handle answer submission. """

    # Get the chosen answer from the form submission and append it to the responses list 
    choice = request.form.get('choice')

    # Get response data from session and update it
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    # Redirect to next question
    return redirect(f'/questions/{question_id}')

@app.route('/thankyou')
def thankyou():
    """
    Render the thank you page if all questions have been answered.
    
    """
    responses = session.get('responses')

    # Redirect to start page if user tries to access completed page without completing the survey
    if responses is None:
        return redirect('/')

    # Redirect to the next unanswered question if all questions have not been answered.
    if len(responses) != len(survey.questions):
        flash('Please answer this question first')
        return redirect(f'/questions/{len(responses)}')

    return render_template('thankyou.html')

@app.route('/session', methods = ["POST"] ) 
def session_view():
    """
    Initialize the session with an empty responses list and start the survey.
    """
    session['responses'] = []

    return redirect(url_for('questions', question_id = 0))




