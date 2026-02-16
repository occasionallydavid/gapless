from flask import Flask, Response, jsonify, send_file
import subprocess
import time
from datetime import datetime

app = Flask(__name__)
start_time = time.time()


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/player')
def player():
    return send_file('player.html')


@app.route('/segment/<int:segment_num>')
def segment(segment_num):
    start_sec = segment_num * 5
    cmd = [
        'ffmpeg', '-v', 'error',
        '-ss', str(start_sec),
        '-t', '5',
        '-i', 'input.aac',
        '-c', 'copy',
        '-f', 'adts',
        '-'
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def generate():
        while True:
            chunk = proc.stdout.read(4096)
            if not chunk:
                break
            yield chunk
        proc.wait()

    return Response(generate(), mimetype='audio/aac')


@app.route('/time')
def server_time():
    now = time.time()
    return jsonify({
        'server_time': datetime.now().isoformat(),
        'server_time_unix': now,
        'uptime_seconds': now - start_time
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
