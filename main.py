import os
import python.MachineLearning as ML
import numpy as NP
from flask import Flask, render_template, request, redirect, url_for
from IPython import embed
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/var/www/uploads"
ALLOWED_EXTENSIONS = set(["jpg", "png", "jpeg", "gif"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_picture():
    if 'picture' not in request.files:
        return redirect(request.url)

    file = request.files['picture']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # file.save(os.path("./python/tempImages"))
        decision = ML.rate(NP.array(file))
        return redirect(url_for('display_result', decision=decision))

@app.route("/result", methods=["GET"])
def display_result():
    embed()
    return render_template("result.html", decision=decision)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run()