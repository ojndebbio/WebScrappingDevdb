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
    mars = mongo.db.mars.find_one()
    return render_template("index.html", data=mars)

# Scrape Route to Import 'scrape_mars.py' Script & Call 'scrape' Function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful"

# Define Main Behavior
if __name__ == "__main__":
    app.run()