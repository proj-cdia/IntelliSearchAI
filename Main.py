from utils.Loader import load_config
from model.Model import *
import os
import warnings  
warnings.filterwarnings("ignore")  
from utils.Logger import save_log


if __name__ == "__main__":
    #ALTERAR DEPOIS
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = ''
    config = load_config("model/config.json")
    model, prompt, = config["model"], config["prompt"] 
    temperature, max_lenght = float(config["temperature"]), int(config["max_lenght"])
    searcher = Model(model, temperature, max_lenght)

    print("Bem vindo ao IntelliSearchAI!")
    while True:
        search = input("Digite sua busca: ")
        anwser = searcher.run(search)
        print("Produtos recomendados: " + anwser)
