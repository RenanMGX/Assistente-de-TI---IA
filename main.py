from Entities.api import ApiRequest
from Entities.credenciais import Credential
from typing import List
import traceback
from time import sleep


lista_exit:List[str] = [
    "Adeus", "Tchau", "Até logo", "Até mais", "Valeu", "Falou", "Fui", "Abraços", "Beijos",
    "Adeusinho", "Nos vemos", "Passar bem", "Ate mais tarde", "Sair", "Xau", "Exit"
]
lista_exit = [item.lower() for item in lista_exit]

if __name__ == "__main__":
    try:
        crd:dict = Credential("TOKEN_GEMINI").load()
        bot = ApiRequest(token=crd["password"])
        
        print(bot.question("Se apresente para o usuario, apenas uma apresentação sobre voce e nada mais"))
        while True:
            entrada:str = input("Digite: ")
            if entrada == "":
                print("\n    Digite algo por favor \n")
                continue
            
            response = bot.question(entrada)

            print(response)
            
            if entrada.lower() in lista_exit:
                break
            sleep(2)
    except Exception as error:
        print(traceback.format_exc())
        input()
        