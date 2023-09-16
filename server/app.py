from flask import Flask,jsonify,request
from flask_cors import CORS
from pymongo import MongoClient
from flask_session import Session

app = Flask(__name__)
app.secret_key="12345"
CORS(app)

client = MongoClient("mongodb+srv://siliang:AA6fDGeHzpg32wMm@communication.qdhodth.mongodb.net/?retryWrites=true&w=majority")
db = client["Communication"]
user_collection = db["User"]

@app.route('/signup',methods=['POST'])
def signUp():
    try:
        if request.method == 'POST':
            # Get data from client and insert into MongoDB
            username = request.json.get('Username', None)
            password = request.json.get('PassWord', None)
            
            if not all([username,password]):
                return jsonify({'status': "status","message":'Missing data'}), 400
            
            if username and password:
                user_collection.insert_one({"Username": username, "PassWord": password})
                return jsonify({"status": "success","message":"SignUp Success"}), 200
            else:
                return jsonify({"status": "failure", "error": "Missing fields"}), 400
    except Exception as e:
        return jsonify({"status": "failure", "error": "not working"}), 500
    
@app.route('/login',methods=['POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.json.get('Username', None)
            password = request.json.get('PassWord', None)
            if not all([username, password]):
                return jsonify({'status': "failure", 'error': 'Missing data'}), 400
            user1 = user_collection.find_one({"Username": username})
            if user1:
                if user1["PassWord"] == password:
                    return jsonify({"status": "success", "message": "SignIn Success"}), 200
                else:
                    return jsonify({"status": "failure", "error": "Password Fail"}), 400
            else:
                return jsonify({"status": "failure", "error": "No User"}), 400
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)