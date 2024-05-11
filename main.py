from Entities.api import ApiRequest
from Entities.credenciais import Credential



if __name__ == "__main__":
    crd:dict = Credential("TOKEN_GEMINI").load()
    bot = ApiRequest(token=crd["password"])
    
    while True:
        response = bot.question(input("Digite: "))
        print(response)