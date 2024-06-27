from flask import Flask, jsonify, request 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['POST'])
def test():
    result = request.json
    print(result)
    return result 

if __name__ == '__main__':
    app.run(host='localhost', port=5000)

