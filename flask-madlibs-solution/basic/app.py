from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension

from stories import silly_story

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)


@app.get("/")
def ask_questions():
    """Generate and show form to ask words."""

    prompts = silly_story.prompts

    return render_template("questions.html", prompts=prompts)


@app.get("/results")
def show_results():
    """Show story result."""

    text = silly_story.generate(request.args)

    return render_template("results.html", text=text)
