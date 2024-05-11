import google.generativeai as genai
from typing import List
from credenciais import Credential

class ApiRequest:
    @property
    def generation_config(self) -> dict:
        return self.__generation_config
    
    @property
    def safety_settings(self) -> List[dict]:
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            ]
        
        return safety_settings

    @property
    def system_instruction(self)  -> str:
        return self.__system_instruction

    @system_instruction.setter
    def system_instruction(self, value:str) -> None:
        self.__system_instruction = str(value)
    
    @property
    def model(self) -> genai.GenerativeModel:
        return self.__model
    
    def __init__(self, *,
                 token:str,
                 system_instruction:str="",
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
        
        self.__system_instruction:str
        if system_instruction:
            self.__system_instruction = system_instruction
        else:
            self.__system_instruction = "Você é um Assistente de TI"
            
        
    def question(self, input:str) -> str:
        MODEL_NAME:str = "gemini-1.5-pro-latest"    
        self.__model:genai.GenerativeModel = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=self.generation_config,  # type: ignore
            system_instruction=self.system_instruction,
            safety_settings=self.safety_settings
            )
        
        try:
            response = self.model.generate_content(input)
            return response.text
        except Exception as error:
            return f"um erro ocorreu ao tentar utilzar a api motivo: \n{error.args}"
    
if __name__ == "__main__":
    crd:dict = Credential("TOKEN_GEMINI").load()
    bot = ApiRequest(token=crd["password"], system_instruction=f"versão do sistema operacional do meu computador Windows 10.0.19045")
    
    response = bot.question("qual é meu sistema operacional")
    print(response)
    
