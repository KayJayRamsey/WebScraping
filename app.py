from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__, template_folder='.')

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars = mongo.db.mars_data.find_one() 
    try:
    # Return template and data
        return render_template("index.html", mars_data=mars)
    except:
        return redirect('/scrape', code=302)


# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    
    

    # Ch
    mongo.db.mars_data.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect('/', code=302) 


if __name__ == "__main__":
    app.run(debug=True)
