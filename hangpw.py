import random
from game import Game

class Hangman(Game):
    def __init__(self, word_list):
        self.lives = 6
        self.word_list = word_list
        self.guessed_letters = []
        self.secret_word = random.choice(self.word_list)
        self.man = [" _________ \n", "|         |\n", "|         0\n", "|        /|\n", "|        /|\\\n", "|        /\n", "|        / \\\n", "|\n"]
        self.man_variation = [[0,1,2,4,6,7,7], [0,1,2,4,5,7,7], [0,1,2,4,7,7,7], [0,1,2,3,7,7,7], [0,1,2,1,7,7,7], [0,1,2,7,7,7,7], [0,1,7,7,7,7,7]]
        self.play()

    def play(self):
        return self.info() + self.game_text()

    def move(self, letter):  
        answer = ""      
        if self.valid_input(letter) and letter in self.secret_word: 
            self.guessed_letters.append(letter)
            answer = self.game_text()
            if self.win():                
                answer += "You win!\n"
                self.lives = 0
            else:
                answer += "Guess a character from the word.\n"
        else:
            self.lives -= 1
            answer = self.game_text()
            answer += "Guess a character from the word.\n"
            if self.game_over():
                answer += "The word was " + self.secret_word
        return answer

    def hidden_word(self):
        masked_word = ""
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                masked_word += letter + " "
            else:
                masked_word += "_ "
        return masked_word
    
    def game_text(self):
        answer = ""
        for man_part in self.man_variation[self.lives]:
            answer += self.man[man_part]
        answer += "\nPassword: "+self.hidden_word()+"\n"
        return answer
    
    def valid_input(self, letter):        
        return len(letter)==1 and letter not in self.guessed_letters

    def win(self):
        found_all_letters = True
        for letter in self.secret_word:
            if letter not in self.guessed_letters:
                found_all_letters = False
        return found_all_letters

    def game_over(self):
        return self.lives == 0
    
    def info(self):
        text = """Test if you can guess a WEAK password!
Guess the bad password from the top 1000 bad passwords of 2017.
Reply to the LAST tweet with a single character guess a digit.\n"""
        return text
