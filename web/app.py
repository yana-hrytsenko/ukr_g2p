from flask import Flask, request, jsonify, send_from_directory
from light_stress import install_lite_stub
install_lite_stub()

from ukr_g2p import transcribe

app = Flask(__name__, static_folder="static", static_url_path="")

MODES = [
    "ukr_phonemic", "ukr_broad", "ukr_narrow",
    "ipa_phonemic", "ipa_broad", "ipa_narrow",
    "eng_friendly",
]


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/transcribe", methods=["POST"])
def api_transcribe():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Type or paste some Ukrainian text first."}), 400
    if len(text) > 500:
        return jsonify({"error": "Keep it under 500 characters for this demo."}), 400

    try:
        results = transcribe(text, mode="all", formatted=False)
    except Exception as exc:  # pipeline can raise on unexpected input
        return jsonify({"error": f"Couldn't transcribe that: {exc}"}), 422

    return jsonify({"text": text, "results": results, "modes": MODES})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
