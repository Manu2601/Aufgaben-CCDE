import requests

host = 'http://localhost:5000/question'

new_question = {
    "level": 1,
    "frageText": "What is the capital of France?",
    "antwortmoeglichkeiten": ["Berlin", "Paris", "London", "Madrid"],
    "richtigeAntwort": "Paris"
}

question_id = 123

print('Hinzufügen einer neuen Frage:')
response = requests.put(f'{host}/{question_id}', json=new_question)

if response.status_code == 200:
    print(response.json()) 
    
    question_id = response.json().get("id")
    if question_id is not None:
        print(f'Hole die Frage mit ID {question_id}:')
        response = requests.get(f'{host}/{question_id}')

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Fehler beim Abrufen der Frage. Statuscode: {response.status_code}")
            
        patch_data = {
            "richtigeAntwort": "NewCorrectAnswer",
            "antwortmoeglichkeiten": ["NewOption1", "NewOption2", "NewOption3", "NewOption4"],
            "frageText": "What is the updated capital of France?",
            "level": 2
        }
        print(f'Patche die Frage mit ID {question_id}:')
        response = requests.patch(f'{host}/{question_id}', json=patch_data)

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Fehler beim Patchen der Frage. Statuscode: {response.status_code}")

        print(f'Lösche die Frage mit ID {question_id}:')
        response = requests.delete(f'{host}/{question_id}')

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Fehler beim Löschen der Frage. Statuscode: {response.status_code}")

    else:
        print("Konnte die Frage-ID nicht abrufen.")
else:
    print(f"Fehler beim Hinzufügen einer neuen Frage. Statuscode: {response.status_code}")
