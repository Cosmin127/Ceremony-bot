from pathlib import Path
import uuid
import os
import traceback

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    jsonify,
)

from main import process_file


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("output")

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/generate")
def generate():
    try:
        print(f"Files: {request.files}")
        print(f"Form: {request.form}")

        if "file" not in request.files:
            print("ERROR: No file in request")
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            print("ERROR: Empty filename")
            return jsonify({"error": "Empty filename"}), 400

        print(f"File received: {file.filename}, size: {len(file.read()) if file else 'unknown'}")

     
        file.seek(0)

        output_type = request.form.get("output", "excel")
        reason = request.form.get("reason", "").strip()
        logged_by = request.form.get("logged_by", "").strip()
        ceremony_type = request.form.get("ceremony_type", "eu_na")

        exclude_clasps = {
            "Bronze": "exclude_bronze" in request.form,
            "Silver": "exclude_silver" in request.form,
            "Gold": "exclude_gold" in request.form,
            "No Clasp": "exclude_no" in request.form,
            "Knappe": "exclude_knappe" in request.form,
            "Ritter": "exclude_ritter" in request.form,
            "Kommandeur": "exclude_kommandeur" in request.form,
            "Großmeister": "exclude_grossmeister" in request.form,
            "Hochmeister": "exclude_hochmeister" in request.form,
        }

        extension = Path(file.filename).suffix.lower()
        upload_path = UPLOAD_FOLDER / f"{uuid.uuid4()}{extension}"
        file.save(upload_path)

        print(f"File saved to: {upload_path}")

        output_file = process_file(
            upload_path,
            output=output_type,
            reason=reason,
            logged_by=logged_by,
            exclude_clasps=exclude_clasps,
            ceremony_type=ceremony_type,
        )

        print(f"Output file: {output_file}")

   
        try:
            os.remove(upload_path)
        except FileNotFoundError:
            pass

        if not output_file.exists():
            print(f"ERROR: Output file not found: {output_file}")
            return jsonify({"error": "Output file was not created"}), 500

        if output_type == "json":
            mimetype = "application/json"
        else:
            mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        response = send_file(
            output_file,
            as_attachment=True,
            download_name=output_file.name,
            mimetype=mimetype,
        )

        @response.call_on_close
        def cleanup():
            try:
                os.remove(output_file)
            except FileNotFoundError:
                pass

        return response

    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5023,
        debug=True,
    )
