import json
"""
Documentação da classe Loader:
    Atributos:
        Caminho do arquivo de configuração do modelo.
        
    Métodos:
        load_config: Método responsável por carregar o arquivo de configuração do modelo.
        retorno:
            Nome do modelo, temperatura, tamanho máximo da resposta e prompt.

"""

def load_config(file_path):  
    with open(file_path) as file:  
        return json.load(file)
    
#load token from .env file

