from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    session,
    send_from_directory,
    jsonify
)

import os
from datetime import datetime

app = Flask(__name__)

app.secret_key = "goutham123"

# -----------------------------
# Configuration
# -----------------------------

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "docx",
    "doc",
    "txt",
    "zip",
    "rar",
    "ppt",
    "pptx",
    "xls",
    "xlsx"
}

USERNAME = "admin"
PASSWORD = "admin123"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -----------------------------
# Allowed File Types
# -----------------------------

def allowed_file(filename):

    return (

        "." in filename

        and

        filename.rsplit(".",1)[1].lower()

        in ALLOWED_EXTENSIONS

    )


# -----------------------------
# File Icon
# -----------------------------

def file_icon(filename):

    ext = filename.rsplit(".",1)[1].lower()

    icons = {

        "pdf":"fa-file-pdf",

        "doc":"fa-file-word",

        "docx":"fa-file-word",

        "xls":"fa-file-excel",

        "xlsx":"fa-file-excel",

        "ppt":"fa-file-powerpoint",

        "pptx":"fa-file-powerpoint",

        "png":"fa-file-image",

        "jpg":"fa-file-image",

        "jpeg":"fa-file-image",

        "txt":"fa-file-lines",

        "zip":"fa-file-zipper",

        "rar":"fa-file-zipper"

    }

    return icons.get(

        ext,

        "fa-file"

    )


# -----------------------------
# Human Readable Size
# -----------------------------

def readable_size(size):

    if size < 1024:

        return f"{size} B"

    elif size < 1024*1024:

        return f"{size/1024:.2f} KB"

    else:

        return f"{size/(1024*1024):.2f} MB"


# -----------------------------
# Dashboard Data
# -----------------------------

def dashboard_data():

    files = []

    total_size = 0

    total_files = 0

    image_count = 0

    document_count = 0

    archive_count = 0

    recent_uploads = []

    for filename in os.listdir(UPLOAD_FOLDER):

        path = os.path.join(

            UPLOAD_FOLDER,

            filename

        )

        if os.path.isfile(path):

            size = os.path.getsize(path)

            total_size += size

            total_files += 1

            ext = filename.rsplit(".",1)[1].lower()

            if ext in [

                "png",

                "jpg",

                "jpeg"

            ]:

                image_count += 1

            elif ext in [

                "pdf",

                "doc",

                "docx",

                "txt",

                "ppt",

                "pptx",

                "xls",

                "xlsx"

            ]:

                document_count += 1

            elif ext in [

                "zip",

                "rar"

            ]:

                archive_count += 1

            files.append({

                "name": filename,

                "size": readable_size(size),

                "raw_size": size,

                "icon": file_icon(filename),

                "date": datetime.fromtimestamp(

                    os.path.getmtime(path)

                ).strftime(

                    "%d-%m-%Y %I:%M %p"

                )

            })

    files.sort(

        key=lambda x:x["raw_size"],

        reverse=True

    )

    recent_uploads = files[:5]

    return {

        "files":files,

        "total_files":total_files,

        "storage":readable_size(total_size),

        "images":image_count,

        "documents":document_count,

        "archives":archive_count,

        "recent":recent_uploads

    }
# ---------------------------------
# Login
# ---------------------------------

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        username = request.form["username"].strip()

        password = request.form["password"].strip()

        if username == USERNAME and password == PASSWORD:

            session["user"] = username

            flash("Welcome Back!")

            return redirect("/")

        flash("Invalid Username or Password!")

        return redirect("/login")

    return render_template("login.html")


# ---------------------------------
# Logout
# ---------------------------------

@app.route("/logout")

def logout():

    session.pop("user", None)

    flash("Logged Out Successfully!")

    return redirect("/login")


# ---------------------------------
# Dashboard
# ---------------------------------

@app.route("/")

def home():

    if "user" not in session:

        return redirect("/login")

    data = dashboard_data()

    return render_template(

        "index.html",

        files=data["files"],

        total_files=data["total_files"],

        storage=data["storage"],

        images=data["images"],

        documents=data["documents"],

        archives=data["archives"],

        recent=data["recent"]

    )


# ---------------------------------
# Search Files
# ---------------------------------

@app.route("/search")

def search():

    if "user" not in session:

        return redirect("/login")

    keyword = request.args.get(

        "q",

        ""

    ).lower().strip()

    data = dashboard_data()

    if keyword != "":

        data["files"] = [

            file

            for file in data["files"]

            if keyword in file["name"].lower()

        ]

    return render_template(

        "index.html",

        files=data["files"],

        total_files=data["total_files"],

        storage=data["storage"],

        images=data["images"],

        documents=data["documents"],

        archives=data["archives"],

        recent=data["recent"]

    )


# ---------------------------------
# Upload File
# ---------------------------------

@app.route("/upload", methods=["POST"])

def upload():

    if "user" not in session:

        return redirect("/login")

    if "file" not in request.files:

        flash("Please Select a File.")

        return redirect("/")

    file = request.files["file"]

    if file.filename == "":

        flash("No File Selected.")

        return redirect("/")

    if not allowed_file(file.filename):

        flash("Unsupported File Type.")

        return redirect("/")

    filename = file.filename

    save_path = os.path.join(

        UPLOAD_FOLDER,

        filename

    )

    if os.path.exists(save_path):

        flash("File Already Exists.")

        return redirect("/")

    file.save(save_path)

    flash("File Uploaded Successfully!")

    return redirect("/")
# ---------------------------------
# Download File
# ---------------------------------

@app.route("/download/<filename>")

def download(filename):

    if "user" not in session:

        return redirect("/login")

    return send_from_directory(

        app.config["UPLOAD_FOLDER"],

        filename,

        as_attachment=True

    )


# ---------------------------------
# Preview File
# ---------------------------------

@app.route("/preview/<filename>")

def preview(filename):

    if "user" not in session:

        return redirect("/login")

    return send_from_directory(

        app.config["UPLOAD_FOLDER"],

        filename

    )


# ---------------------------------
# Delete File
# ---------------------------------

@app.route("/delete/<filename>")

def delete(filename):

    if "user" not in session:

        return redirect("/login")

    path = os.path.join(

        UPLOAD_FOLDER,

        filename

    )

    if os.path.exists(path):

        os.remove(path)

        flash("File Deleted Successfully!")

    else:

        flash("File Not Found!")

    return redirect("/")


# ---------------------------------
# Share Link
# ---------------------------------

@app.route("/share/<filename>")

def share(filename):

    if "user" not in session:

        return redirect("/login")

    link = request.host_url + "preview/" + filename

    return jsonify({

        "link": link

    })


# ---------------------------------
# Dashboard API
# ---------------------------------

@app.route("/dashboard-data")

def dashboard_api():

    if "user" not in session:

        return jsonify({"error":"Unauthorized"}),401

    data = dashboard_data()

    return jsonify({

        "total_files":data["total_files"],

        "storage":data["storage"],

        "images":data["images"],

        "documents":data["documents"],

        "archives":data["archives"]

    })


# ---------------------------------
# Recent Uploads API
# ---------------------------------

@app.route("/recent")

def recent():

    if "user" not in session:

        return redirect("/login")

    data = dashboard_data()

    return jsonify(data["recent"])
# ---------------------------------
# Delete All Files
# ---------------------------------

@app.route("/reset")

def reset():

    if "user" not in session:

        return redirect("/login")

    deleted = 0

    for filename in os.listdir(UPLOAD_FOLDER):

        path = os.path.join(

            UPLOAD_FOLDER,

            filename

        )

        if os.path.isfile(path):

            os.remove(path)

            deleted += 1

    flash(f"{deleted} Files Deleted Successfully!")

    return redirect("/")


# ---------------------------------
# Storage Information API
# ---------------------------------

@app.route("/storage")

def storage():

    if "user" not in session:

        return jsonify({"error":"Unauthorized"}),401

    total_size = 0

    total_files = 0

    for filename in os.listdir(UPLOAD_FOLDER):

        path = os.path.join(

            UPLOAD_FOLDER,

            filename

        )

        if os.path.isfile(path):

            total_files += 1

            total_size += os.path.getsize(path)

    return jsonify({

        "total_files": total_files,

        "storage_used": readable_size(total_size)

    })


# ---------------------------------
# Custom 404 Page
# ---------------------------------

@app.errorhandler(404)

def page_not_found(error):

    return render_template(

        "404.html"

    ),404


# ---------------------------------
# Custom 500 Page
# ---------------------------------

@app.errorhandler(500)

def internal_error(error):

    return render_template(

        "500.html"

    ),500


# ---------------------------------
# Health Check
# ---------------------------------

@app.route("/health")

def health():

    return {

        "status":"OK",

        "project":"Cloud File Storage System",

        "version":"Premium 2.0"

    }


# ---------------------------------
# Run Application
# ---------------------------------

if __name__ == "__main__":

    app.run(

        debug=True

    )