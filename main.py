import os
import python.MachineLearning as ML
import python.ScreenShotTaker as SS
import numpy as NP
from skimage import io
from flask import Flask, render_template, request, redirect, url_for
from IPython import embed

UPLOAD_FOLDER = "/var/www/uploads"
ALLOWED_EXTENSIONS = set(["jpg", "png", "jpeg", "gif"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    url = request.form['url']
    screen_shot = SS.takeScreenShot("http://" + url)
    decision = ML.rate(io.imread("static/temp.png"))
    return render_template("result.html", decision=decision)

if __name__ == "__main__":
    app.run()