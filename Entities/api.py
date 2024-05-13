import google.generativeai as genai
from typing import List
from datetime import datetime
try:
    from Entities.pc_config_collect import ConfigPC
except:
    from pc_config_collect import ConfigPC
from time import sleep
import requests
from bs4 import BeautifulSoup
import requests

def formatar_site(url:str) -> str:
    try:
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        formated = ""
        for line in soup.get_text().split("\n"):
            if line:
                formated += line
        return formated
    except:
        return "Não Identificado"
        

portifolio_renan = formatar_site("https://renanmgx.github.io/")

github_renan = formatar_site("https://github.com/RenanMGX")



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
        _system_instruction:str = f""
        _system_instruction += f"Nome: Orion; "
        _system_instruction += f"Data Criação do Orion: 11/05/2024 - 05:32:12 am"
        _system_instruction += f"Ocupação: Assistente de Suporte de TI; "
        _system_instruction += f"Descrição do trabalho: Orion é responsável por auxiliar usuários, incluindo aqueles com pouca experiência técnica, na resolução de problemas relacionados à tecnologia da informação (TI). Ele é capacitado para pesquisar na internet em busca de soluções. Orion lida com uma variedade de questões, incluindo problemas de hardware, software, redes, segurança e configurações de sistemas. Ele também está familiarizado com sistemas operacionais como Windows, macOS e Linux, e tem experiência em suporte a aplicativos de produtividade, como pacotes de escritório e ferramentas de colaboração. Além disso, Orion pode ajudar a configurar e solucionar problemas relacionados a dispositivos móveis, impressoras e outros dispositivos periféricos.; "
        _system_instruction += f"Despedida: Ao receber a despedida do usuário, responda com uma mensagem de despedida e finalize com '--> FIM DO PROGRAMA <--'.;"
        _system_instruction += f"Informações da máquina do usuário:\n {'{'}{ConfigPC()}{'}'}, "
        _system_instruction += f"Sempre consulte as 'Informações da máquina do usuário' antes de responder a qualquer pergunta. Evite solicitar mais informações ao usuário sobre os itens da lista, pois ele pode não ter conhecimento dela. Um script em Python coleta as informações e envia a lista.; "
        _system_instruction += f"Data Atual: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}; "
        _system_instruction += f"Criador: Seu modelo de IA está sendo utilizado por uma API. Quem desenvolveu esse script chama-se Renan Brian, GitHub: https://github.com/RenanMGX/, Linkedin: https://www.linkedin.com/in/renanmgx/, Site Portifolio: https://renanmgx.github.io, email: renanmgx@hotmail.com;"
        _system_instruction += f"Infor: Aqui está o link para o repositório online e aberto do código-fonte do Orion no GitHub: https://github.com/RenanMGX/Assistente-de-TI---IA.;"
        _system_instruction += f"Infor Criador: Codigo HTML do portifolio do Renan Brian {portifolio_renan}, Codigo HTML do portifolio do Renan Brian {portifolio_renan}; "
        return _system_instruction

    
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
            return f"\nOrion: \n{response.text}\n"
        except Exception as error:
            if "Resource has been exhausted (e.g. check quota)." in error.args:
                return "\n    Muitas perguntas em pouco tempo, espere um pouco e tente novamente!\n "
            elif "HARM_CATEGORY_HARASSMENT" in str(error.args):
                return "\n    O Conteudo perguntado não é apropriado\n"
            return f"um erro ocorreu ao tentar utilzar a api motivo: \n{error.args}"
    
if __name__ == "__main__":
    
    # from credenciais import Credential
    # crd:dict = Credential("TOKEN_GEMINI").load()
    bot = ApiRequest(token="TOKEN")
    print(bot.system_instruction)
    #print(formatar_site("https://renanmgx.github.io/"))
    # response = bot.question("qual é meu sistema operacional")
    # print(response)
    
