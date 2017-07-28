
from flask import Flask, render_template
from db import get_cities_and_tags, get_json

app = Flask(__name__)

# Note having this here means that these variables will only be updated when the app restarts
# Will need to add code to update them without restarting the app

@app.route("/")
def home_page():
    cities, tags = get_cities_and_tags()
    return render_template("landing.html", cities=cities, tags=tags)

@app.route("/get_data/<city>/<tag>")
def serve_subs(city, tag):
    return get_json(city, tag)
