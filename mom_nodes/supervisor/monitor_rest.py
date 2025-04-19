
# mom_nodes/supervisor/monitor_rest.py

from flask import Flask, jsonify
from message_backup import get_backup_messages

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Supervisor is active"}), 200

@app.route("/backup", methods=["GET"])
def get_backup():
    return jsonify(get_backup_messages()), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
