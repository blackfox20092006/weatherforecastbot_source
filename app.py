from flask import Flask, request, jsonify
from flask_cors import CORS
from api_module import get_answer

app = Flask(__name__)
CORS(app)

@app.route('/get_answer', methods=['GET'])
def answer():
    data = request.args.get('question')
    _response_ = get_answer(data)
    return jsonify(answer=_response_)
if __name__ == '__main__':
    app.run()
