"""FRC Concept Scorer - Flask dev server (use static/app.js for Pages deploy).

Scoring logic lives in scorer.py and is shared with the static JS port.
"""
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from scorer import WEIGHTS, score_concept

DATA_FILE = Path(__file__).parent / "data.json"

app = Flask(__name__)


def load_data() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"concepts": [], "weights": WEIGHTS}


def save_data(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/concepts", methods=["GET"])
def list_concepts():
    data = load_data()
    rows = [
        {**c, "score": score_concept(c, data["weights"])}
        for c in data["concepts"]
    ]
    rows.sort(key=lambda r: r["score"], reverse=True)
    return jsonify({"concepts": rows, "weights": data["weights"]})


@app.route("/api/concepts", methods=["POST"])
def add_concept():
    payload = request.get_json(force=True)
    name = (payload.get("name") or "").strip()
    description = (payload.get("description") or "").strip()
    scores = payload.get("scores") or {}
    if not name or len(scores) != 4:
        return jsonify({"error": "name and 4 scores required"}), 400
    for k, v in scores.items():
        try:
            f = float(v)
        except (TypeError, ValueError):
            return jsonify({"error": f"score {k} must be numeric"}), 400
        if not 0 <= f <= 10:
            return jsonify({"error": f"score {k} must be in [0,10]"}), 400
    data = load_data()
    data["concepts"].append({"name": name, "description": description, "scores": scores})
    save_data(data)
    return jsonify({"ok": True}), 201


@app.route("/api/concepts/<int:idx>", methods=["DELETE"])
def delete_concept(idx: int):
    data = load_data()
    if 0 <= idx < len(data["concepts"]):
        data["concepts"].pop(idx)
        save_data(data)
        return jsonify({"ok": True})
    return jsonify({"error": "not found"}), 404


@app.route("/api/weights", methods=["PUT"])
def update_weights():
    payload = request.get_json(force=True)
    data = load_data()
    for k in WEIGHTS:
        if k in payload:
            try:
                data["weights"][k] = float(payload[k])
            except (TypeError, ValueError):
                return jsonify({"error": f"weight {k} must be numeric"}), 400
    save_data(data)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
