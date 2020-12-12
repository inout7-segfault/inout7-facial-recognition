from logging.config import dictConfig
from predict import find_student
from flask import Flask, redirect, render_template, request
from PIL import Image

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(levelname)s - %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["wsgi"],
        },
    }
)


app = Flask(__name__)


@app.route("/capture")
def capture():
    return render_template("capture.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        image = request.files["image"]

        image = Image.open(image)

        roll_no, name = find_student(image)

    return render_template("upload.html")


if __name__ == "__main__":
    from livereload import Server

    server = Server(app.wsgi_app)
    server.serve(port=5000)
