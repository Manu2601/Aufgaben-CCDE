from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from dataclasses import dataclass
import random
from sqlalchemy import Column, Integer, Text, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///data/millionaire.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()

app = Flask(__name__)
api = Api(app)

class Millionaire(Base):
    __tablename__ = 'millionaire'

    id = Column(Integer, primary_key=True)
    difficulty = Column(Integer)
    question = Column(Text)
    correct_answer = Column(Text)
    answer2 = Column(Text)
    answer3 = Column(Text)
    answer4 = Column(Text)
    background_information = Column(Text)

    def serialize(self):
        return {'id': self.id,
                'difficulty': self.difficulty,
                'question': self.question,
                'correct_answer': self.correct_answer
                }

diff = 0
@app.route('/')
def home():
    global m
    m = Millionaire.query.filter(Millionaire.difficulty == diff).order_by(func.random()).first()
    answers = [m.correct_answer, m.answer2, m.answer3, m.answer4]
    random.shuffle(answers) 
    return render_template('millionaire.html', question=m.question, answers=answers)

class QuestionService(Resource):
    def get(self, question_id):
        question = Millionaire.query.get(question_id)
        if question:
            return jsonify(question.serialize())
        return {"Message": f"Question with id {question_id} not found"}, 404

    def put(self, question_id):
        data = request.get_json(force=True)
        question = Millionaire.query.get(question_id)
        if question:
            question.difficulty = data.get('difficulty', question.difficulty)
            question.question = data.get('question', question.question)
            question.correct_answer = data.get('correct_answer', question.correct_answer)
            question.answer2 = data.get('answer2', question.answer2)
            question.answer3 = data.get('answer3', question.answer3)
            question.answer4 = data.get('answer4', question.answer4)
            db_session.commit()
            return {"Message": f"Question with id {question_id} updated"}
        return {"Message": f"Question with id {question_id} not found"}, 404

    def delete(self, question_id):
        question = Millionaire.query.get(question_id)
        if question:
            db_session.delete(question)
            db_session.commit()
            return {"Message": f"Question with id {question_id} deleted"}
        return {"Message": f"Question with id {question_id} not found"}, 404

    def patch(self, question_id):
        data = request.get_json(force=True)
        question = Millionaire.query.get(question_id)
        if question:
            question.difficulty = data.get('difficulty', question.difficulty)
            question.question = data.get('question', question.question)
            question.correct_answer = data.get('correct_answer', question.correct_answer)
            question.answer2 = data.get('answer2', question.answer2)
            question.answer3 = data.get('answer3', question.answer3)
            question.answer4 = data.get('answer4', question.answer4)
            db_session.commit()
            return {"Message": f"Question with id {question_id} patched"}
        return {"Message": f"Question with id {question_id} not found"}, 404


@app.route('/answer/<string:answer>')
def answer(answer):
    global diff 
    current_question = m 
    if current_question.correct_answer == answer:
        diff = diff+1
        if diff>=5:
            diff = 0
            return render_template('feedback.html', feedback="Du hast gewonnen! Gratulation!")
        return render_template('feedback.html', feedback="Richtige Antwort!", diff=f"Dein aktuelles Level ist {diff}!")
    else:
        diff = 0
        return render_template('feedback.html', feedback=F"Leider falsch, die richtige Antwort wäre: {m.correct_answer}", diff=f"Dein aktuelles Level ist {diff}!")

class RandomQuestionService(Resource):
    def get(self):
        random_question = Millionaire.query.order_by(func.random()).first()
        return jsonify(random_question.serialize())

class AllQuestionsService(Resource):
    def get(self):
        questions = Millionaire.query.all()
        return jsonify([question.serialize() for question in questions])

api.add_resource(QuestionService, '/question/<int:question_id>')
api.add_resource(RandomQuestionService, '/random_question')
api.add_resource(AllQuestionsService, '/all_questions')

if __name__ == '__main__':
    app.run(debug=True)
