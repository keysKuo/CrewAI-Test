from flask import Flask, jsonify, request 
from flask_cors import CORS
from test_local import generate

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['POST'])
def test():
    req = request.json
    question = req['question']
    schema = req['schema']
    memory = req['memory']

    # print(memory)

    result = generate(question, schema, memory)
    return result

if __name__ == '__main__':
    app.run(host='localhost', port=5000)

