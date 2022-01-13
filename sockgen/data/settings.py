from sockgen.metaclass.singleton import Singleton

class Settings(metaclass=Singleton): 
    def __init__(self):
        self.theme = 'calm'
        self.configFile = None