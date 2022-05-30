from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Create an app, being sure to pass __name__
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Define what to do when a user goes to the index route
@app.route("/")
def index():
   marsinfo = mongo.db.mars.find_one()
   return render_template("index.html", mars=marsinfo)

# Define what to do when a user goes to the /about route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

   
if __name__ == "__main__":
   app.run()