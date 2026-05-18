from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Create upload folder
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------- Validation ----------
def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

# ---------- Home ----------
@app.route("/")
def index():
    images = os.listdir(UPLOAD_FOLDER)

    return render_template(
        "index.html",
        images=images
    )

# ---------- Upload ----------
@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return redirect("/")

    file = request.files["image"]

    if file.filename == "":
        return redirect("/")

    if file and allowed_file(file.filename):
        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

    return redirect("/")

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
