from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

from stories import stories

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)


@app.get("/")
def ask_story():
    """Show list-of-stories form."""

    return render_template("select-results.html",
                           stories=stories.values())


@app.get("/questions")
def ask_questions():
    """Generate and show form to ask words."""

    story_code = request.args["story_code"]
    story = stories[story_code]

    prompts = story.prompts

    return render_template("questions.html",
                           story_code=story_code,
                           title=story.title,
                           prompts=prompts)


@app.get("/<story_code>/results")
def show_results(story_code):
    """Show story result."""

    story = stories[story_code]

    text = story.generate(request.args)

    return render_template("results.html",
                           title=story.title,
                           text=text)
