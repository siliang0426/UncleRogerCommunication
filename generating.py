import csv
import random

# Define the headers
headers = ["Patient name", "Disease", "Symptom", "Blood Pressure", "Cholesterol", "White Cell"]

# Define some sample data for diseases, symptoms, etc.
names = ["Alice", "Bob", "Charlie", "David", "Emily", "Fiona", "George", "Helen", "Ian", "Jack"]
surnames = ["Johnson", "Smith", "Brown", "Williams", "Davis", "Green", "King", "Miller", "White", "Lee"]
diseases = ["Flu", "Asthma", "Diabetes", "High Blood Pressure", "Common Cold", "Anemia"]
severe_disease = ["Hantavirus Infection", "COVID-19" ]
low_disease = ["Lupus", "Ebola", "Measles"]
symptoms = {
    "Flu": ["Fever", "Cough", "Sore Throat"],
    "Asthma": ["Shortness of Breath", "Wheezing"],
    "Diabetes": ["Increased Thirst", "Increased Hunger"],
    "High Blood Pressure": ["Headache", "Dizziness"],
    "Common Cold": ["Runny Nose", "Sneezing"],
    "Anemia": ["Fatigue", "Weakness"],
    "Lupus": ["Malar Rash", "Discoid Rash", "Photosensitivity", "Oral or Nose Ulcers", "Kidney Disorder"],
    "Hantavirus Infection": ["Bleeding", "Fever", "Headaches", "Muscle Aches", "Abdominal Pain", "Kidney Failure"],
    "Ebola": ["Fever", "General Malaise and weakness", "Muscle and Joint Pains", "Anorexia", "Diarrhea", "Vomiting", "Fluid Lost"],
    "COVID-19": ["Fever", "Chills", "Cough", "Difficulty Breathing", "Fatigue", "Loss of Taste", "Loss of Smell", "Nausea"],
    "Measles": ["Fever", "Cough", "Runny Nose", "Red, Watery Eyes", "Red, Sore Eyes", "Swollen Eyes", "Aches and Pains", "Weakness", "Hacking Cough", "Total Body Skin Rash"]
}

### lupus and ebola can be low
### hantavirus, covid is high

# Generate random data for 100 patients
data = [headers]
for i in range(100):
    name = f"{random.choice(names)} {random.choice(surnames)}"
    white_cell = str(random.randint(2000, 18000))

    if(white_cell > "11000"):
        temp = random.choice(severe_disease)
    elif(white_cell < "4000"):
        temp = random.choice(low_disease)
    else:
        temp = random.choice(diseases)
        
    symptom = ", ".join(random.sample(symptoms[disease], 2))
    blood_pressure = f"{random.randint(90, 160)}/{random.randint(60, 100)}"
    cholesterol = str(random.randint(150, 240))

    data.append([name, temp, symptom, blood_pressure, cholesterol, white_cell])

# Write to CSV
with open('patients.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',')
    for row in data:
        csv_writer.writerow(row)
