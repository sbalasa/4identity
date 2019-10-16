"""
A sample webserver to launch 4identity client app via smartconnect in order to sign a document.

To run:
python webapp.py
"""
import os
import shutil


from flask import Flask, flash, request, render_template


UPLOAD_FOLDER = "./static"
HOST = "192.168.56.102"
LICENSE_DNS_NAME = "testserverbit.com"
PORT = "8080"
CONNECTOR_PATH = "/opt/bit4id/connector"
DOCUMENT_FILENAME = ""

app = Flask(__name__, static_url_path="/static")
app.secret_key = "webapptest"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        uploaded_file = request.files["uploaded_file"]
        if uploaded_file:
            global DOCUMENT_FILENAME
            DOCUMENT_FILENAME = uploaded_file.filename
            uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], DOCUMENT_FILENAME))
            document_path = f"http://{HOST}:{PORT}/static/{DOCUMENT_FILENAME}"
            return render_template("file_upload.html", document_path=document_path, filename=DOCUMENT_FILENAME)
        else:
            return render_template("404.html")
    return render_template("welcome.html")


@app.route("/webapptest/smartengine/end-sign", methods=["GET", "POST"])
def uploaded():
    shutil.copy(f"{CONNECTOR_PATH}/var/test_output/webapptest/test.pdf", f"./static/signed-{DOCUMENT_FILENAME}")
    return render_template("success.html", path=f"http://{LICENSE_DNS_NAME}:{PORT}/static/signed-{DOCUMENT_FILENAME}")


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
