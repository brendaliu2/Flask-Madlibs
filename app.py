from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

from stories import silly_story

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)




@app.get('/')
def questions():
    """takes story instance prompts and creates form to display"""
    questions = silly_story.prompts
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