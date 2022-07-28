from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

from stories import silly_story, excited_story

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)


@app.get('/')
def load_home_page():
    '''displays drop down form to choose story template'''

    return render_template('homepage.html')

@app.get('/questions')
def questions():
    """takes story instance prompts and creates form to display"""
    story_type = request.args["story-type"]
    questions = globals()[story_type].prompts
    return render_template('questions.html',
                            questions = questions)


@app.get('/results')
def results():
    '''takes inputs from form and generate story to display'''
    # answers = {}
    # questions = silly_story.prompts
    # for question in questions:
    #     answers[question] = request.args[question] #can just pass in request.args
    text = silly_story.generate(request.args)
    return render_template('results.html',
                            text = text)