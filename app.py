import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from predict import predict

# ======================================
# Konfigurasi Flask
# ======================================

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ======================================
# Cek Ekstensi File
# ======================================

def allowed_file(filename):

    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ======================================
# Halaman Utama
# ======================================

@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    image_path = None
    error = None

    if request.method == "POST":

        if "image" not in request.files:

            error = "Silakan pilih gambar."

            return render_template(
                "index.html",
                error=error
            )

        file = request.files["image"]

        if file.filename == "":

            error = "File belum dipilih."

            return render_template(
                "index.html",
                error=error
            )

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(filepath)

            image_path = filepath

            result = predict(filepath)

        else:

            error = "Format gambar harus JPG, JPEG, atau PNG."

    return render_template(
        "index.html",
        result=result,
        image_path=image_path,
        error=error
    )


# ======================================
# Run Flask
# ======================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )