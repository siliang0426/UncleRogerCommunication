from flask import Flask, jsonify, redirect, url_for, request, render_template, abort
from flask_cors import CORS
from pymongo import MongoClient
from collections import Counter
from bson.objectid import ObjectId
import csv
import re
import openai
import os
import gridfs
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = "a456P77"  # Set secret key
CORS(app)

openai.api_key = "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"
client = MongoClient("mongodb+srv://jiaming:9R65kJIHzJOC2e5i@cluster0.akhyses.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")
db = client["Communication"]
user_collection = db["User"]
question_collection = db["Questions"]
answer_collection = db["Answer"]
fs = gridfs.GridFS(db)

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
with open('reasources/patients.csv', 'r') as csvfile:
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
        if disease not in freq_disease_symptoms:
            freq_disease_symptoms[disease] = []
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
    try:
        if request.method == 'POST':
            text_content = request.form.get('textContent')
            uploaded_file = request.files.get('file')  # Use get to avoid KeyError
            
            file_id = None  # Initialize to None
            
            if uploaded_file and uploaded_file.filename != '':
                file_id = fs.put(uploaded_file, filename=uploaded_file.filename)
                
            question = {"question": text_content, "file_id": file_id}
            
            question_collection.insert_one(question)
            qb = question_collection.find_one({"question": text_content})
            answer_collection.insert_one({"questionID": qb['_id'],"answer":None})
            return jsonify({"status": "success", "message": "Question submit Success"}), 200
    except Exception as e:
        print("Error: ", e)  # Log the exception for debugging
        return jsonify({"status": "failure", "error": "fail to return question"}), 500

@app.route('/question_display',methods=['GET'])
def question_display():
    try:
        if request.method == 'GET':
            question = question_collection.find_one()
            if question is None:
                return jsonify({"status": "failure", "error": "question not found"}), 500
            question_message = question['question']
            question_id = question['_id']
            question_id = str(question_id)

            response = {
                'message': question_message,
                'question_id':question_id
            }
            
            return jsonify(response), 200
    except Exception as e:
        print("Error: ", e)  # Log the exception for debugging
        return jsonify({"status": "failure", "error": "fail to return question"}), 500


@app.route('/answer2Question', methods=['POST'])
def answer2Question():
    try:
            
        if request.method == 'POST':
            questionID = request.json.get("question_id")
            questionID = ObjectId(questionID)
            question = question_collection.find_one({"_id":questionID})

            if not question:
                return jsonify({"status": "failure", "error": "No question found"}), 404
            
            
            respond = request.json.get('respond', None)
            if not respond:
                return jsonify({"status": "failure", "error": "No response provided"}), 400
            
            existing_answer = answer_collection.find_one({"q_id": questionID})

            if existing_answer:
                # If the answer already exists, update it
                answer_collection.update_one(
                    {"q_id": questionID},
                    {"$push": {"DrAnswer.responds": respond}}
                )
            else:
                # If the answer doesn't exist, create a new document
                answer_collection.insert_one(
                    {"q_id": questionID, "DrAnswer": {"responds": [respond]}}
                )
            
            return jsonify({"status": "success", "question_id": str(questionID)}), 200
            
    except Exception as e:
        print("Error: ", e)  # Log the exception for debugging
        return jsonify({"status": "failure", "error": "An error occurred"}), 500
    
@app.route('/GPTReport', methods=['POST'])
def GPTReport():
    questionID = request.json.get("question_id",None)
    questionID = ObjectId(questionID)
    answers = answer_collection.find_one({"_id":questionID})
    # Create a prompt that includes the disease-symptom pattern and the doctor's answer
    prompt = "Disease-Symptom Database:\n"

    for disease, symptoms in freq_disease_symptoms.items():
        prompt += f"{disease}: {', '.join(symptoms)}\n"

    prompt += "\nDoctor's Observation:\n"
    if answers:
        responses = answers.get('DrAnswers', {}).get('response', [])
    
        for response in responses:
            prompt+=response
    prompt += "\n\nPlease generate a report and suggestion arounds 100 words based on the observation."

    # Generate the report
    response = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo-0613",
        messages=[{'role':'assistant','content':prompt}],
        max_tokens=1000
    )
    
    report = response['choices'][0]['message']['content']
    return jsonify({"report":report})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)