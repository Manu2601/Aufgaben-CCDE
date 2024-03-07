import requests
import json

host = 'http://localhost:5000/question'

def get_question(question_id):
    print(f'Hole die Frage mit ID {question_id}:')
    response = requests.get(f'{host}/{question_id}')
    return response

def update_question(question_id, update_data):
    print(f'Update der Frage mit ID {question_id}:')
    response = requests.put(f'{host}/{question_id}', json=update_data)
    return response

def patch_question(question_id, patch_data):
    print(f'Patchen der Frage mit ID {question_id}:')
    response = requests.patch(f'{host}/{question_id}', json=patch_data)
    return response

def delete_question(question_id):
    print(f'Lösche die Frage mit ID {question_id}:')
    response = requests.delete(f'{host}/{question_id}')
    return response

if __name__ == "__main__":
    new_question = {
        "difficulty": 1,
        "question": "What is the capital of France?",
        "correct_answer": "Paris",
        "answer2": "Berlin",
        "answer3": "London",
        "answer4": "Madrid",
        "background_information": "Paris is the capital of France."
    }

question_id = 123
if question_id:
            get_response = get_question(question_id)
            if get_response.status_code == 200:
                print(get_response.json())
            
            # Frage aktualisieren
            update_data = {
                "difficulty": 2,
                "question": "What is the updated capital of France?",
                "correct_answer": "Paris",
                "answer2": "Berlin",
                "answer3": "London",
                "answer4": "Madrid",
                "background_information": "Updated background information."
            }
            update_response = update_question(question_id, update_data)
            if update_response.status_code == 200:
                print(update_response.json())
            
            # Frage patchen
            patch_data = {
                "background_information": "Additional updated background information."
            }
            patch_response = patch_question(question_id, patch_data)
            if patch_response.status_code == 200:
                print(patch_response.json())

            # Frage löschen
            delete_response = delete_question(question_id)
            if delete_response.status_code == 200:
                print(delete_response.json())
else:
            print("Konnte die Frage-ID nicht abrufen.")
