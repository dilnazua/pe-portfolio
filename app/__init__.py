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
    education_text_dilnaz
)

load_dotenv("./example.env")
app = Flask(__name__)


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


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


def mapping(coords):
    markers = ""

    for id, (lat, lon) in enumerate(coords):
        # Create the marker and its pop-up for each shop
        idd = f"a{id}"
        markers += "var {idd} = L.marker([{latitude}, {longitude}]);\
                            {idd}.addTo(map);".format(
            idd=idd,
            latitude=lat,
            longitude=lon,
        )
    return coords, markers


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
        (37.7749, -122.4194)
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


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/api/timeline_post", methods=["DELETE"])
def delete_timeline_post():
    timeline_post = (
        TimelinePost.select().order_by(TimelinePost.created_at.desc()).first()
    )
    if timeline_post:
        timeline_post.delete_instance()
        return jsonify({"message": "Last timeline post deleted"})
    else:
        abort(404)


@app.route('/timeline', methods=["GET", "POST"])
def timeline():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        timeline_post = TimelinePost.create(name=name, email=email, content=content)

    timeline_posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template('timeline.html', title="Timeline", timeline_posts=timeline_posts)


if __name__ == "__main__":
    app.run()
