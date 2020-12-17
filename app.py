import numpy as np
from flask import Flask, render_template, request
from PIL import Image

import datetime

from predict import find_student
from database import add_attendance

app = Flask(__name__)

slot = 1

@app.route("/capture")
def capture():
    return render_template("capture.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    global slot
    if request.method == "POST":
        image = request.files["image"]

        # course = request.files["course"]
        # slot = request.files["slot"]
        course = "CS510"
        slot+=1
        image = Image.open(image)

        student_details = find_student(np.array(image))

        add_attendance(student_id=student_details["Roll_num"],date = datetime.date.today(),course=course,slot=slot)

        print(f"present : {student_details['Name']} with acc : {student_details['accuracy']}")

    return render_template("upload.html")


if __name__ == "__main__":
    from livereload import Server

    server = Server(app.wsgi_app)
    server.serve(port=5000)
