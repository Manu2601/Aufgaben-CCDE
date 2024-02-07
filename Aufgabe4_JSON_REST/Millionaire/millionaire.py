from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from dataclasses import dataclass
import random

app = Flask(__name__)
api = Api(app)

@dataclass
class Question:
    id: int
    level: int
    frageText: str
    antwortmoeglichkeiten: list
    richtigeAntwort: str

questions = {}

def load_questions():
    with open("Millionaire\\data\\millionaire.txt", "r") as file:
        next(file)
        
        question_id_counter = 0

        for line in file:
            data = line.strip().split('\t')

            if len(data) < 6 or not data[1] or not data[2] or not data[3] or not data[4] or not data[5]:
                continue

            level = int(data[0])
            frage_text = data[1]
            antwortmoeglichkeiten = [data[2], data[3], data[4], data[5]]
            richtige_antwort = data[2]

            questions[question_id_counter] = Question(
                id=question_id_counter,
                level=level,
                frageText=frage_text,
                antwortmoeglichkeiten=antwortmoeglichkeiten,
                richtigeAntwort=richtige_antwort
            )

            question_id_counter += 1

load_questions()
        
class QuestionService(Resource):
    def get(self, question_id):
        if question_id in questions:
            return jsonify(questions[question_id].__dict__)
        return {"Message": f"Question with id {question_id} not found"}, 404

    def put(self, question_id):
        data = request.get_json(force=True)
        questions[question_id] = Question(
            id=question_id,
            level=data['level'],
            frageText=data['frageText'],
            antwortmoeglichkeiten=data['antwortmoeglichkeiten'],
            richtigeAntwort=data['richtigeAntwort']
        )
        return {"id": question_id, "Message": f"Question with id {question_id} saved"}

    def delete(self, question_id):
        if question_id in questions:
            del questions[question_id]
            return {"Message": f"Question with id {question_id} deleted"}
        return {"Message": f"Question with id {question_id} not found"}, 404

    def patch(self, question_id):
        data = request.get_json(force=True)
        if question_id in questions:
            if 'richtigeAntwort' in data:
                questions[question_id].richtigeAntwort = data['richtigeAntwort']
            if 'antwortmoeglichkeiten' in data:
                questions[question_id].antwortmoeglichkeiten = data['antwortmoeglichkeiten']
            if 'frageText' in data:
                questions[question_id].frageText = data['frageText']
            if 'level' in data:
                questions[question_id].level = data['level']
            return {"Message": f"Question with id {question_id} patched"}
        return {"Message": f"Question with id {question_id} not found"}, 404

class RandomQuestionService(Resource):
    def get(self):
        random_id = random.choice(list(questions.keys()))
        return jsonify(questions[random_id].__dict__)

class AllQuestionsService(Resource):
    def get(self):
        return jsonify([question.__dict__ for question in questions.values()])

api.add_resource(QuestionService, '/question/<int:question_id>')
api.add_resource(RandomQuestionService, '/random_question')
api.add_resource(AllQuestionsService, '/all_questions')

if __name__ == '__main__':
    app.run(debug=True)
