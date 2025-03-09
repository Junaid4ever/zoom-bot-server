from flask import Flask, request, jsonify
import subprocess
import threading

app = Flask(__name__)

def run_zoom_bot(meeting_id, password, num_users):
    command = f"python3 bot.py {meeting_id} {password} {num_users}"
    subprocess.Popen(command, shell=True)

@app.route("/start", methods=["POST"])
def start_bots():
    data = request.json
    meeting_id = data.get("meetingID")
    password = data.get("password")
    num_users = data.get("numUsers")

    if not meeting_id or not password or not num_users:
        return jsonify({"error": "Missing parameters"}), 400

    threading.Thread(target=run_zoom_bot, args=(meeting_id, password, num_users)).start()
    return jsonify({"message": "Bots started!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
