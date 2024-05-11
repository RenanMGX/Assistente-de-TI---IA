# Documentação do Programa

## Introdução
Este programa é um assistente de TI baseado em inteligência artificial que pode responder a várias perguntas relacionadas a computadores. Ele utiliza a API Gemini para gerar respostas inteligentes.

## Requisitos
Antes de executar o programa, certifique-se de ter instalado todas as dependências listadas no arquivo `requirements.txt`.

## Estrutura do Projeto
O projeto é dividido em várias partes, cada uma representada por um módulo Python.

- `main.py`: Script principal que interage com o usuário.
- `Entities/api.py`: Módulo que lida com as solicitações à API Gemini.
- `Entities/credenciais.py`: Módulo para manipulação de credenciais.
- `Entities/pc_config_collect.py`: Módulo para coleta de informações do sistema.
- `Entities/__init__.py`: Arquivo para garantir que o Python reconheça o diretório como um pacote.

## Como Usar
Para usar o programa, execute o script `main.py` e siga as instruções exibidas no terminal. Aqui está uma visão geral do processo:

1. Inicie o programa fornecendo as credenciais necessárias.
2. O assistente de TI se apresentará e aguardará suas perguntas.
3. Faça perguntas sobre configurações de computador ou problemas relacionados a TI.
4. O assistente responderá com respostas geradas pela inteligência artificial.

Exemplo de uso:

```bash
python main.py
```

# Descrição dos Módulos
### main.py
O script principal interage com o usuário e envia as perguntas para o assistente de TI. Ele também contém a lista de saída para terminar o programa.

### Entities/api.py
Este módulo lida com a comunicação com a API Gemini. Ele fornece uma classe ApiRequest que encapsula a lógica de envio de solicitações e recebimento de respostas.

### Entities/credenciais.py
Este módulo é responsável por carregar e salvar credenciais de acesso à API Gemini. Ele fornece a classe Credential para gerenciar as credenciais.

### Entities/pc_config_collect.py
Este módulo coleta informações do sistema, como especificações do processador, uso da CPU, RAM, armazenamento, etc. Ele fornece a classe ConfigPC para acessar essas informações.

# Considerações Finais
Este programa é uma ferramenta útil para obter respostas rápidas e precisas sobre questões relacionadas a TI. Sinta-se à vontade para explorar e adaptar o código conforme necessário para atender às suas necessidades.

