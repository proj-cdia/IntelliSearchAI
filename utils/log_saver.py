import json
"""
responsável por salvar os dados de entrada e saída do modelo em um arquivo JSON.
  Atributos:
    question: String que contém a pergunta feita pelo usuário.
    answers: String que contém a resposta gerada pelo modelo.
      
  Métodos:
    log_data: Método responsável por salvar os dados de entrada e saída do modelo em um arquivo JSON.
"""
def save_log(question, answer):  
    log = {'Pergunta': question, 'Respostas': answer}    
  
    try:  
        with open('log/log.json', 'r', encoding='utf-8') as file:  
            logs = json.load(file)   
    except (FileNotFoundError, json.JSONDecodeError):  
        logs = []  
  
    logs.append(log)  
    with open('log/log.json', 'w', encoding='utf-8') as file:  
        json.dump(logs, file, indent=4, ensure_ascii=False)

 