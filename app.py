from flask import Flask, render_template, request, redirect, flash, send_from_directory, session
import os

app = Flask(__name__)
app.secret_key = "goutham123"

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "docx"}

USERNAME = "admin"
PASSWORD = "admin123"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

    files = os.listdir(UPLOAD_FOLDER)

    return render_template("index.html", files=files)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:

            session["user"] = username

            flash("Login Successful!")

            return redirect("/")

        else:

            flash("Invalid Username or Password!")

            return redirect("/login")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.pop("user", None)

    flash("Logged Out Successfully!")

    return redirect("/login")


@app.route("/upload", methods=["POST"])
def upload():

    if "user" not in session:
        return redirect("/login")

    file = request.files["file"]

    if file.filename == "":

        flash("Please select a file!")

        return redirect("/")

    if allowed_file(file.filename):

        file.save(os.path.join(UPLOAD_FOLDER, file.filename))

        flash("File Uploaded Successfully!")

    else:

        flash("Invalid file type! Only PDF, JPG, JPEG, PNG and DOCX files are allowed.")

    return redirect("/")


@app.route("/view/<filename>")
def view(filename):

    if "user" not in session:
        return redirect("/login")

    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/download/<filename>")
def download(filename):

    if "user" not in session:
        return redirect("/login")

    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route("/delete/<filename>")
def delete(filename):

    if "user" not in session:
        return redirect("/login")

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):

        os.remove(file_path)

        flash("File Deleted Successfully!")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)