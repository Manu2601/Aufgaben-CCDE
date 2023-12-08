import random

class Question:
    def __init__(self):
        self._fragen = []
        self._level = 0
        self._current_question = None

    def readQuestions(self, fName):
        with open(fName, 'r') as file:
            lines = file.readlines()
            for line in lines:
                question = line.strip().split('\t')
                if len(question) >= 1 and question[0].isdigit():
                    self._fragen.append({
                        "level": int(question[0]),
                        "frageText": question[1],
                        "antwortmoeglichkeiten": question[2:6],
                        "richtigeAntwort": question[2]
                    })

    def getRandomQuestion(self):
        filtered_questions = [q for q in self._fragen if q["level"] == self._level]
        if filtered_questions:
            self._current_question = random.choice(filtered_questions)
            return self._current_question
        return None

    def getCurrentQuestion(self):
        return self._current_question