from Entities.api import ApiRequest
from Entities.token_admin import TokenAdmin
from typing import List
import traceback
from time import sleep
import sys
sys.path.append("Entities")
import multiprocessing
multiprocessing.freeze_support()


vesion="1.1"


if __name__ == "__main__":
    try:
        token:TokenAdmin = TokenAdmin("token_gemini")
        crd:str = token.load()
        if not crd:
            print(f"Não foi encontrado um token no arquivo {token.file}")
            entrada = input("Digite um Token valido: ")
            token.save(entrada)
            print("token registrado!")
            crd = token.load()        
        
        
        
        print(f"Iniciando Programa versão {vesion}...")
        bot = ApiRequest(token=crd)
        bot.start()
        
        print("#"*50)
        print(bot.question("Apresente-se para o usuário sem fornecer informações sobre a máquina, e compartilhe uma interessante sobre um assunto atual."))
        
        while True:
            print("#"*50)
            entrada:str = input("Digite: ")
            if entrada == "":
                print("\n    Digite algo por favor \n")
                continue
            
            response = bot.question(entrada)

            print(str(response).replace("--> FIM DO PROGRAMA <--", ""))
            
            # if entrada.lower() in lista_exit:
            #     break
            if "--> FIM DO PROGRAMA <--" in str(response):
                sleep(6)
                break
            
            sleep(2)
    except Exception as error:
        print(traceback.format_exc())
        input()
        