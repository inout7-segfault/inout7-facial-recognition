from logging.config import dictConfig

import flask_uploads
from flask import Flask, redirect, render_template, request

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


photos = flask_uploads.UploadSet(
    name="photos", extensions=flask_uploads.IMAGES, default_dest=lambda _: "photos"
)
flask_uploads.configure_uploads(app, [photos])
flask_uploads.patch_request_class(app=app, size=4 * 1024 * 1024)


@app.route("/capture")
def capture():
    return render_template("capture.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "capture" in request.files:
        filename = photos.save(request.files["capture"])
        path_to_file = photos.path(filename)
        app.logger.info(path_to_file)

    return render_template("upload.html")


if __name__ == "__main__":
    from livereload import Server

    server = Server(app.wsgi_app)
    server.serve(port=5000)
