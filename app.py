from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://<dbuser>:<dbpassword>@ds123770.mlab.com:23770/heroku_0c0nt9gr"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars = mongo.db.listings.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.listings
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("//", code=302)

if __name__ == "__main__":
    app.run(debug=True)
