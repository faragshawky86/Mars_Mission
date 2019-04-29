from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/nasa_app")

@app.route("/")
def home():

    # Find one record of data from the mongo database
    db_data = mongo.db.mars_data.find_one()
    print('---------------------------')

    print("DB_DATA: ", db_data)
    print('---------------------------')

    # return jsonify(True)

    # Return template and data
    return render_template("index.html", mars_data = db_data)


@app.route("/scraped")
def scraped():
    #drops collection for duplicates
    mongo.db.mars_data.drop()
    # Run the scrape function

    all_mars_data = {
    "mars_news_title": scrape.scrape_mars_nasa(),
    "mars_jpl_data": scrape.scrape_mars_jpl(),
    "mars_weather_data": scrape.scrape_mars_weather(),
    "hemisphere_image_urls": scrape.get_hemisphere_img(),
    "mars_html": scrape.get_mars_html()
    }
    print('---------------------------')

    print("SCRAPED DATA: ", all_mars_data)

    print('---------------------------')

    #Insert the Mongo database 
    mongo.db.mars_data.insert(all_mars_data)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)