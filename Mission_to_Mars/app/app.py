from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape import scrape

# Flask Setup
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Flask Routes

# Query Root to  MongoDB & Pass Mars Data Into HTML (index.html) Template
@app.route("/")
def index():
    NASA = mongo.db.mars.find_one()
    NASA = scrape()
    return render_template("index.html", data=NASA)

# Scrape Route to Import 'scrape.py' Script & Call 'scrape' Function
@app.route("/scrape")
def scraper():
    NASA = scrape()
    mars = mongo.db.mars
    mars.update({}, NASA, upsert=True)
    # return render_template("index.html", data=NASA)
    return redirect("/", code=302)

# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)