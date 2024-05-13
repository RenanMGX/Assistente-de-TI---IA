import google.generativeai as genai
from typing import List
from datetime import datetime
try:
    from Entities.pc_config_collect import ConfigPC
except:
    from pc_config_collect import ConfigPC
from time import sleep

import requests

portifolio_renan:str
try:
    portifolio_renan = requests.get("https://renanmgx.github.io/").text
except:
    portifolio_renan = "não identificado"

github_renan:str
try:
    github_renan = requests.get("https://github.com/RenanMGX").text
except:
    github_renan = "não identificado"


class ApiRequest:
    @property
    def generation_config(self) -> dict:
        return self.__generation_config
    
    @property
    def safety_settings(self) -> List[dict]:
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },            
            ]
        
        return safety_settings

    
    #propriedade com instruçoes para a IA
    @property
    def system_instruction(self)  -> str:        
        _system_instruction:str = f"""
        Nome: Orion;\n
        Ocupação: Assistente de Suporte de TI;\n
        Descrição do trabalho: Orion é responsável por auxiliar usuários, incluindo aqueles com pouca experiência técnica, na resolução de problemas relacionados à tecnologia da informação (TI). Ele é capacitado para pesquisar na internet em busca de soluções. Orion lida com uma variedade de questões, incluindo problemas de hardware, software, redes, segurança e configurações de sistemas. Ele também está familiarizado com sistemas operacionais como Windows, macOS e Linux, e tem experiência em suporte a aplicativos de produtividade, como pacotes de escritório e ferramentas de colaboração. Além disso, Orion pode ajudar a configurar e solucionar problemas relacionados a dispositivos móveis, impressoras e outros dispositivos periféricos.;\n
        Despedida: Por favor, sinta-se à vontade para se despedir quando estiver pronto. Assim que você se despedir. Se isso acontecer, termine a interação com '--> FIM DO PROGRAMA <--'.;
        Criador: Seu modelo de IA está sendo utilizado por uma API. Quem desenvolveu esse script chama-se Renan Brian, GitHub: https://github.com/RenanMGX/Assistente-de-TI---IA, Linkedin: https://www.linkedin.com/in/renanmgx/, Site Portifolio: https://renanmgx.github.io/#home;
        Infor Criador: Codigo HTML do portifolio do Renan Brian {portifolio_renan}, Codigo HTML do portifolio do Renan Brian {portifolio_renan}; 
        Informações da máquina do usuário:\n {ConfigPC()};\n
        Sempre deve consultar as "Informações da máquina do usuário" antes de responder qualquer pergunta\n
        Data Atual: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}
        """,         # type: ignore
        
        
        
        return _system_instruction

    @system_instruction.setter
    def system_instruction(self, value:str) -> None:
        self.__system_instruction = str(value)
    
    @property
    def model(self) -> genai.GenerativeModel:
        return self.__model
    
    @property
    def chat(self):
        return self.__chat
    
    def __init__(self, *,
                 token:str,
                 temperature:float|int=1,
                 top_p:float|int=0.95,
                 top_k:float|int=0,
                 max_output_tokens:float|int=8192
                 ) -> None:
        """Classe construtora, recebe os parametros necessarios para construir uma boa requisição para a api

        Args:
            token (str): token de utilização do gemini
            system_instruction (str, optional): instruçoes da api define um comportamento para a ia. Defaults to "".
            temperature (float | int, optional): de 0 a 1 define a aleatoriedade das resposta 1 é mais aleatorio. Defaults to 1.
            top_p (float | int, optional): _description_. Defaults to 0.95.
            top_k (float | int, optional): _description_. Defaults to 0.
            max_output_tokens (float | int, optional): _description_. Defaults to 8192.
        """
        
        genai.configure(api_key=token)
        
        self.__generation_config:dict = {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "max_output_tokens": max_output_tokens,
        }
        
        
    def start(self):
        MODEL_NAME:str = "gemini-1.5-pro-latest"    
        self.__model:genai.GenerativeModel = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=self.generation_config,  # type: ignore
            system_instruction=self.system_instruction,
            safety_settings=self.safety_settings
            )
            
        self.__chat = self.model.start_chat(history=[])
            
        
    def question(self, input:str) -> str:
        try:
            prompt:str = input
            response = self.chat.send_message(prompt)
            return f"\nAssistente:\n{response.text}\n"
        except Exception as error:
            if "Resource has been exhausted (e.g. check quota)." in error.args:
                return "\n    Muitas perguntas em pouco tempo, espere um pouco e tente novamente!\n "
            elif "HARM_CATEGORY_HARASSMENT" in str(error.args):
                return "\n    O Conteudo perguntado não é apropriado\n"
            return f"um erro ocorreu ao tentar utilzar a api motivo: \n{error.args}"
    
if __name__ == "__main__":
    pass
    # from credenciais import Credential
    # crd:dict = Credential("TOKEN_GEMINI").load()
    # bot = ApiRequest(token=crd["password"])
    
    # response = bot.question("qual é meu sistema operacional")
    # print(response)
    
