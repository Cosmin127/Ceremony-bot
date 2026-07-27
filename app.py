from pathlib import Path
import uuid
from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
)
import os
from main import generate_excel

app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("output")

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


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

    extension = Path(file.filename).suffix.lower()

    upload_path = UPLOAD_FOLDER / f"{uuid.uuid4()}{extension}"

    file.save(upload_path)

    result = generate_excel(upload_path)

    # Delete the uploaded .txt
    try:
        os.remove(upload_path)
    except FileNotFoundError:
        pass

    response = send_file(
        result["output"],
        as_attachment=True,
        download_name=result["output"].name,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # Delete the generated Excel after it's been sent
    @response.call_on_close
    def cleanup():

        try:
            os.remove(result["output"])
        except FileNotFoundError:
            pass

    return response

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5023,
        debug=True,
    )
