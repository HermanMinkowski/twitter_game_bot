import random
from game import Game

class Guess_number(Game):
    def __init__(self):
        self.lives = 3
        self.secret_number = str(random.randint(1,9))
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] 

        self.play()

    def play(self):
        return  self.info()

    def move(self, number):        
        answer = ""
        if number not in self.numbers:
            answer = "Not a valid number. Game Over!"
            self.lives  = 0
        else:
            if number == self.secret_number:
                self.lives  = 0
                answer = "You won!"
            else:
                self.lives-=1
                if(self.lives == 0):
                    answer = "Game Over! The number was "+ str(self.secret_number)
                else:
                    answer = "Try again. You have %s chances left" % self.lives        
        return answer

    def game_over(self):
        return self.lives == 0

    def info(self):
        text = """How to play:\n
- Guess a number from 1 to 10. You have 3 chances.\n
- Reply to the LAST tweet with a single number.\n"""
        return text
