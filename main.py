from Entities.api import ApiRequest
from Entities.credenciais import Credential



if __name__ == "__main__":
    crd:dict = Credential("TOKEN_GEMINI").load()
    bot = ApiRequest(token=crd["password"], system_instruction="")
    bot.system_instruction = "windows 10"
    
    response = bot.question("qual é o sistema operacional")
    print(response)