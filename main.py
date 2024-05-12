from Entities.api import ApiRequest
from Entities.credenciais import Credential
from typing import List
import traceback
from time import sleep


if __name__ == "__main__":
    try:
        crd:dict = Credential("TOKEN_GEMINI").load()
        if not crd["password"]:
            print("""
                    Não existe um token no arquivo crd/TOKEN_GEMINI.json\n
                    1ª solução: Durante a instanciação do ApiRequest, coloque seu token como exemplo: ApiRequest(token="SEU_TOKEN")\n
                    2ª solução: Utilize o gerenciador de credenciais para salvar e ocultar seu token. Como usar:\n
                    Execute o método crd.save(user="QUALQUER_VALOR", password="SEU_TOKEN"). Ele irá salvar o token em um arquivo crd/TOKEN_GEMINI.json\n
                    Depois, pode ser consultado utilizando o método crd.load(), que irá retornar um dicionário com user= e password= salvos no arquivo.\n
                  """)
            exit()
        
        bot = ApiRequest(token=crd["password"])
        bot.start()
        
        print(bot.question("Apresente-se para o usuário sem fornecer informações sobre a máquina, e compartilhe uma interessante sobre um assunto atual."))
        while True:
            entrada:str = input("Digite: ")
            if entrada == "":
                print("\n    Digite algo por favor \n")
                continue
            
            response = bot.question(entrada)

            print(str(response).replace("--> FIM DO PROGRAMA <--", ""))
            
            # if entrada.lower() in lista_exit:
            #     break
            if "--> FIM DO PROGRAMA <--" in str(response):
                break
            
            sleep(2)
    except Exception as error:
        print(traceback.format_exc())
        input()
        