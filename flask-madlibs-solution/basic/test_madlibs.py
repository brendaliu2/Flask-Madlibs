import app as app_module
from app import app
from unittest import TestCase

from stories import Story

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app_module.silly_story = Story(
    ['animal', 'color'],
    "The {animal} is {color}"
)


class MadlibsViewsTestCase(TestCase):
    def test_question_form(self):
        with app.test_client() as client:
            resp = client.get("/")
            body = resp.get_data(as_text=True)

            self.assertRegex(body, r"<input\s+name=['\"]animal['\"]")
            self.assertRegex(body, r"<input\s+name=['\"]color['\"]")

    def test_result_story(self):
        answers = dict(animal="pika", color="pink")

        with app.test_client() as client:
            resp = client.get("/results", query_string=answers)
            body = resp.get_data(as_text=True)

            self.assertIn("The pika is pink", body)
