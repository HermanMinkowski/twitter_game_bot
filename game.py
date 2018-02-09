import abc
class Game(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def play(self):
        pass
    @abc.abstractmethod
    def move(self, movement):
        pass
    @abc.abstractmethod
    def game_over(self):
        pass
    @abc.abstractmethod
    def info(self):
        pass
