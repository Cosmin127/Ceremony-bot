from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
)

from main import generate_excel

app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


@app.get("/")
def index():

    return render_template("index.html")


@app.post("/generate")
def generate():

    if "file" not in request.files:
        return redirect("/")

    file = request.files["file"]

    if file.filename == "":
        return redirect("/")

    upload_path = UPLOAD_FOLDER / file.filename

    file.save(upload_path)

    result = generate_excel(upload_path)

    return send_file(
        result["output"],
        as_attachment=True,
        download_name=result["output"].name,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
