import os

class TokenAdmin:
    @property
    def path(self):
        return "crd/"
    
    @property
    def file(self):
        value:str = self.__file
        if not value.endswith(".txt"):
            value += ".txt"
        return value
    
    def __init__(self, file_name:str) -> None:
        self.__file:str = self.path + file_name
        
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(self.file):
            with open(self.file, 'w')as _file:
                _file.write("")
                
    def load(self) -> str:
        with open(self.file, 'r')as _file:
            return _file.read()
        
    def save(self, value:str) -> str:
        value = str(value)
        with open(self.file, 'w')as _file:
            _file.write(value)
        


if __name__ == "__main__":
    bot = TokenAdmin("token_gemini")

    
    print(bot.load())