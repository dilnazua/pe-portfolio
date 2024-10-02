import os
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
from flask import Flask, render_template, request
from dotenv import load_dotenv
from flask import jsonify, abort, Response
import re
from app.text import (
    about_text,
    work_text_dilnaz,
    about_text_dilnaz,
    work_text,
    education_text,
    education_text_dilnaz,
    gensler_info,
    minerva_info,
    mlh_info,
    google_info,
    uber_info
)

# Load environment variables from .env file
load_dotenv("./example.env")
app = Flask(__name__)

# Check if running in testing mode
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )


# Define a Peewee model for Timeline Posts
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

# Connect to the database and create tables if necessary
mydb.connect()
mydb.create_tables([TimelinePost])

# Function to map coordinates to markers for the map
def mapping(coords):
    markers = ""

    for id, (lat, lon) in enumerate(coords):
        # Create markers for each coordinate
        idd = f"a{id}"
        markers += "var {idd} = L.marker([{latitude}, {longitude}]);\
                            {idd}.addTo(map);".format(
            idd=idd,
            latitude=lat,
            longitude=lon,
        )
    return coords, markers

# Route for the homepage
@app.route("/")
def index():
    coords = [
        (48.0196, 66.9237),
        (61.5240, 105.3188),
        (41.3775, 64.5853),
        (38.9637, 35.2433),
        (37.0902, -95.7129),
        (51.1694, 71.4491),
        (43.2220, 76.8512),
        (47.1097, 51.9104),
        (42.9026, 71.3656),
        (51.2333, 51.3667),
        (45.0158, 78.3673),
        (43.6481, 51.1706),
        (43.6028, 39.7342),
        (53.1959, 50.1002),
        (40.7128, -74.0060),
        (36.9741, -122.0308),
        (34.0522, -118.2437),
        (41.2995, 69.2401),
        (36.7664, 31.3870),
        (36.8969, 30.7133),
        (37.3875, -122.0575),
        (37.7749, -122.4194),
        (52.5200, 13.4049),
        (50.0755, 14.4378),
        (41.9028, 12.4964),
        (40.8518, 14.2681),
        (48.8566, 2.3522),
        (43.7696, 11.2558),
        (44.4949, 11.3426),
        (37.5665, 126.9780)
        
    ]

    # Render the page with the map
    return render_template(
        "index.html",
        markers=mapping(coords)[1],
        lat=(mapping(coords))[0][0][0],
        lon=(mapping(coords))[0][0][1],
        title="Dilnaz Uasheva",
        url=os.getenv("URL"),
        photo="dilnaz",
        about_text=about_text_dilnaz,
        work_text=work_text_dilnaz,
        education_text=education_text_dilnaz,
        gensler_info=gensler_info[0],
        minerva_info=minerva_info[0],
        mlh_info=mlh_info[0],
        google_info=google_info[0],
        uber_info=uber_info[0]
    )


@app.route("/hobbies")
def hobbies():
    title = "Our Team's Hobbies"
    hobbies_list = [
        {"title": "Reading", "image": "static/img/reading.jpg"},
        {"title": "Gardening", "image": "static/img/gardening.jpg"},
        {"title": "Painting", "image": "static/img/painting.jpg"},
        {"title": "Cooking", "image": "static/img/cooking.jpg"},
    ]

    return render_template("hobbies.html", title=title, hobbies_list=hobbies_list)

# Route to create a new timeline post (POST request)
@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    name = request.form.get("name", None)
    if not name or not bool(re.match("[a-zA-z]*", name)):
        return jsonify({"Error": "Invalid name"}), 400
    email = request.form.get("email", None)
    if not email or "@" not in email:
        return jsonify({"Error": "Invalid email"}), 400
    content = request.form.get("content", None)
    if not content:
        return jsonify({"Error": "Invalid content"}), 400
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

# Route to get all timeline posts (GET request)
@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

# Route to delete the last timeline post (DELETE request)
@app.route("/api/timeline_post", methods=["DELETE"])
def delete_timeline_post():
    # Get the last timeline post by creation date
    timeline_post = (
        TimelinePost.select().order_by(TimelinePost.created_at.desc()).first()
    )
    if timeline_post:
        # Delete the instance of the timeline post
        timeline_post.delete_instance()
        return jsonify({"message": "Last timeline post deleted"})
    else:
        # If no timeline post is found, return a 404 error
        abort(404)


# Route for the timeline page with GET and POST requests
@app.route('/timeline', methods=["GET", "POST"])
def timeline():
    if request.method == "POST":
        # If the request method is POST, create a new timeline post
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        timeline_post = TimelinePost.create(name=name, email=email, content=content)

    # Retrieve all timeline posts and order by creation date descending
    timeline_posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template('timeline.html', title="Timeline", timeline_posts=timeline_posts)


@app.route("/cportfolio")
def cportfolio():
    coords = [
        (48.0196, 66.9237),
        (61.5240, 105.3188),
        (41.3775, 64.5853),
        (38.9637, 35.2433),
        (37.0902, -95.7129),
        (51.1694, 71.4491),
        (43.2220, 76.8512),
        (47.1097, 51.9104),
        (42.9026, 71.3656),
        (51.2333, 51.3667),
        (45.0158, 78.3673),
        (43.6481, 51.1706),
        (43.6028, 39.7342),
        (53.1959, 50.1002),
        (40.7128, -74.0060),
        (36.9741, -122.0308),
        (34.0522, -118.2437),
        (41.2995, 69.2401),
        (36.7664, 31.3870),
        (36.8969, 30.7133),
        (37.3875, -122.0575),
        (37.7749, -122.4194),
        (52.5200, 13.4049),
        (50.0755, 14.4378),
        (41.9028, 12.4964),
        (40.8518, 14.2681),
        (48.8566, 2.3522),
        (43.7696, 11.2558),
        (44.4949, 11.3426),
        (37.5665, 126.9780)
    ]

    return render_template(
        "index.html",
        markers=mapping(coords)[1],
        lat=(mapping(coords))[0][0][0],
        lon=(mapping(coords))[0][0][1],
        title="Dilnaz Uasheva - CPortfolio",
        url=os.getenv("URL"),
        photo="dilnaz",
        about_text=about_text_dilnaz,
        work_text=work_text_dilnaz,
        education_text=education_text_dilnaz,
        gensler_info=gensler_info[0],
        minerva_info=minerva_info[0],
        mlh_info=mlh_info[0],
        google_info=google_info[0],
        uber_info=uber_info[0]
    )

# Run the app if this script is executed directly
if __name__ == "__main__":
    app.run()
    
