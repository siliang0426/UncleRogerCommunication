from flask import Flask,jsonify,request
from flask_cors import CORS
from pymongo import MongoClient
from flask_session import Session
import re

app = Flask(__name__)
app.secret_key="12345"
CORS(app)

client = MongoClient("mongodb+srv://jiaming:9R65kJIHzJOC2e5i@cluster0.akhyses.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")
db = client["Communication"]
user_collection = db["User"]

#writing stopword
stopword = []
stopwords_file_path="reasources/stopwords.txt"
with open(stopwords_file_path, 'r') as f:
    for line in f:
    # Tokenize the line into words.
        words = line.strip().split()
    # Update word frequencies.
        for word in words:
            stopword.append(word.lower())
    

def get_keywords_from_file(filename):
    HiFreqWord = {}

    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
        words = re.split(r'[ .,!;\n\t]+', text)
        words = [word for word in words if word]
        for word in words:
            if word.lower() in HiFreqWord:
                HiFreqWord[word.lower()]+=1
            else:
                HiFreqWord[word.lower()]=1
                
    filtered_HiFreqWord = {k: v for k, v in HiFreqWord.items() if k not in stopword}
    sorted_HiFreqWord = sorted(filtered_HiFreqWord.items(), key=lambda x: x[1], reverse=True)
    top_10_HiFreqWord = sorted_HiFreqWord[:10]
   
    return top_10_HiFreqWord[:10]  # Take first 10 keywords


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
                user_collection.insert_one({
                    "Username": username,
                    "PassWord": password
                    })
                
                
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


@app.route('/patient_history',methods=['POST'])
def patient_history():
    
    return jsonify({"status": "failure", "error": "not implemented yet"}), 500


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)