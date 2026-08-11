from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app)

REGION_NAME = "ap-south-1"
DEFAULT_BUCKET = "my-file-storage-pavni"

s3 = boto3.client(
    "s3",
    region_name=REGION_NAME
)

@app.route("/generate-url")
def generate_url():
    bucket = request.args.get("bucket", DEFAULT_BUCKET).strip()
    filename = request.args.get("filename", "").strip()

    if not bucket:
        return jsonify({"error": "Bucket name is required."}), 400

    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    print(f"Generating upload URL for bucket={bucket}, filename={filename}")

    url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket,
            "Key": filename
        },
        ExpiresIn=3600
    )

    object_url = f"https://my-file-storage-pavni.s3.ap-south-1.amazonaws.com/{quote_plus(filename)}"

    return jsonify({
        "upload_url": url,
        "object_url": object_url
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)