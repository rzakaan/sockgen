from message_generator.metaclass.singleton import Singleton

class Settings():
    __metaclass__ = Singleton
  
    def __init__(self):
        self.theme = 'calm'
