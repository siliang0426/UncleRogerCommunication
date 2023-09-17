from flask import Flask,jsonify,request
from flask_cors import CORS
from pymongo import MongoClient
from flask_session import Session
from collections import Counter
import csv
import re
import openai

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

freq_disease_symptoms = {}
disease_symptoms = {}
with open('patients.csv', 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Skip the header row

    for row in csv_reader:
        name, disease, symptom, bp, cholesterol, wc = row
        symptoms = [s.strip() for s in symptom.split(",")]  # Split by comma and strip whitespace
        
            # Populate the dictionary
        if disease not in disease_symptoms:
            disease_symptoms[disease] = []
        disease_symptoms[disease].extend(symptoms)

# Count the symptoms for each disease
for disease, symptoms in disease_symptoms.items():
    count_symptoms = Counter(symptoms)
    for symptom, count in count_symptoms.most_common():
        freq_disease_symptoms[disease].append(symptom)


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
    top_5_HiFreqWord = sorted_HiFreqWord[:5]
   
    return top_5_HiFreqWord[:5]  # Take first 10 keywords


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


@app.route('/question',methods=['POST'])
def question():
          
    return jsonify({"status": "failure", "error": "not implemented yet"}), 500


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)