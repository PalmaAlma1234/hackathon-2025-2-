from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/admin/ping')
def ping():
    return jsonify({'status': 'ok', 'app': 'QazKids Flask demo'})


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    # В реальном приложении нужно валидировать подпись и обрабатывать payload
    return jsonify({'received': data or {}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
