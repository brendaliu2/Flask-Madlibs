import app as app_module
from app import app
from unittest import TestCase

from stories import Story

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

story_1 = Story(
    "test_1",
    "Animal Story",
    ['animal', 'color'],
    "The {animal} is {color}"
)
story_2 = Story(
    "test_2",
    "Noun Story",
    ['noun', 'adj'],
    "The {noun} is {adj}"
)
app_module.stories = {"test_1": story_1, "test_2": story_2}


class MadlibsViewsTestCase(TestCase):
    def test_story_form(self):
        with app.test_client() as client:
            resp = client.get("/")
            body = resp.get_data(as_text=True)
            self.assertIn("test_1", body)
            self.assertIn("test_2", body)

    def test_questions_form(self):
        with app.test_client() as client:
            resp = client.get("/questions?story_code=test_1")
            body = resp.get_data(as_text=True)

            self.assertRegex(body, r"<input\s+name=['\"]animal['\"]")
            self.assertRegex(body, r"<input\s+name=['\"]color['\"]")

            resp = client.get("/questions?story_code=test_2")
            body = resp.get_data(as_text=True)

            self.assertRegex(body, r"<input\s+name=['\"]noun['\"]")
            self.assertRegex(body, r"<input\s+name=['\"]adj['\"]")

    def test_result_story(self):
        answers_1 = dict(animal="pika", color="pink")
        answers_2 = dict(animal="teapot", color="stately")

        with app.test_client() as client:
            resp = client.get("/test_1/results", query_string=answers_1)
            body = resp.get_data(as_text=True)
            self.assertIn("The pika is pink", body)

            resp = client.get("/test_1/results", query_string=answers_2)
            body = resp.get_data(as_text=True)
            self.assertIn("The teapot is stately", body)
