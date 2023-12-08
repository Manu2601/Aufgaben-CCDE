import random

class Question:
    def __init__(self, path):
        self._path = path
        self._frageText = ""
        self._level = 0
        self._antwortmoeglichkeiten = []
        self._richtigeAntwort = ""
        self._gameOver = False
        
    def getRandoQuestion(self):
        lines = open(self._path, 'r').readlines()
        while True:
            question = random.choice(lines)
            questionSplit = question.split('\t')
            if questionSplit[0] == str(self._level):
                self._frageText = questionSplit[1]
                self._antwortmoeglichkeiten = [questionSplit[2], questionSplit[3], questionSplit[4], questionSplit[5]]
                random.shuffle(self._antwortmoeglichkeiten)
                self._richtigeAntwort = questionSplit[2]
                break
        
    def __str__(self):
        text = f"-----------------------------------------------------------\nYour current level is {self._level}\n{self._frageText}\n"
        index = 0
        for möglichkeit in self._antwortmoeglichkeiten:
            text += f"({str(index)}) {möglichkeit.removesuffix("\n")}\n"
            index+=1
        text += "Which answer? (0, 1, 2, 3): "
        return text

if __name__ == '__main__':
    question = Question('C:\\Users\\Raffl Manuel\\OneDrive - HTL Anichstrasse\\HTL\\4AHWII\\CCDE\\Python\\Aufgabe05\\millionaire.txt')
    
    while question._gameOver == False:
        question.getRandoQuestion()
        print(question)
        antwort = input() 
        if antwort == str(question._antwortmoeglichkeiten.index(question._richtigeAntwort)):
            print("Correct answer!")
            if question._level < 4:
                question._level += 1
        else:
            print(f"False answer, the correct one was {question._richtigeAntwort}")
            question._gameOver = True
            print("Do you want to start a new game? (yes/no)")
            if input() == "yes":
                question._gameOver = False
                question._level = 0