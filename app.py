#!flask/bin/python
from flask import Flask, jsonify
import auto_grade as ag
from flask import request


app = Flask(__name__)

result = {
        'User': 'manirv',
        'Lab': 'Lab1',
        'labresult': 'PASS',
        'score': 5
    }

@app.route('/rf/api/v1.0/labs', methods=['GET'])
def get_labs():
    return jsonify({'result': result})

@app.route('/rf/api/v1.0/lab', methods=['POST'])
def post_lab():
    content = request.get_json()
    #print(content)
    result = ag.auto_grade(content['userid'],content['labname'], content['code'])
    return jsonify({'result': result})

@app.route('/rf/api/v1.0/key', methods=['POST'])
def post_key():
    content = request.get_json()
    #print(content)
    result = ag.save_lab_key(content['labname'], content['code'])
    return jsonify({'result': result})



if __name__ == '__main__':
    app.run(debug=True)