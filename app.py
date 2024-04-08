from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Machine learning service!'


@app.route('/accept_data', methods=['POST'])
def accept_data():
    return 'Will accept data here to be trained!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
