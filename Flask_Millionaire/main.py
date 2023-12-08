import random
from flask import Flask, render_template
from model.Question import Question

app = Flask(__name__)
question = Question()
question.readQuestions('C:\\Users\\Raffl Manuel\\OneDrive - HTL Anichstrasse\\HTL\\4AHWII\\CCDE\\Python\\Aufgaben CCDE\\Flask_Millionaire\\data\\millionaire.txt')

@app.route('/millionaire')
def home():
    selected_question = question.getRandomQuestion()
    if selected_question:
        frageText = selected_question["frageText"]
        antwortmoeglichkeiten = selected_question["antwortmoeglichkeiten"]
        random.shuffle(antwortmoeglichkeiten)
        return render_template('millionaire.html', question=frageText, answers=antwortmoeglichkeiten)
    return "Keine Frage verfügbar für das aktuelle Level."

@app.route("/question/<int:answer>")
def antwort(answer):
    current_question = question.getCurrentQuestion()

    if current_question:
        richtigeAntwort = current_question["richtigeAntwort"]
        if richtigeAntwort == str(current_question["antwortmoeglichkeiten"][answer - 1]):
            question._level += 1
            if question._level >= 5:
                question._level = 0
                return render_template('feedback.html', feedback="Du hast gewonnen! Gratulation!")
            return render_template('feedback.html', feedback=f"Richtige Antwort, dein aktuelles Level ist {question._level}")

        question._level = 0
        return render_template('feedback.html', feedback=f"Leider falsch, die richtige Antwort wäre: {richtigeAntwort}")

    return "Keine Frage verfügbar für das aktuelle Level."

@app.route("/questions")
def fragen():
    return render_template("questions.html", questions=question._fragen)

if __name__ == '__main__':
    app.run(debug=True)
