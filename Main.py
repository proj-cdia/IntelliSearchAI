from utils.config_loader import load_config
from model.Model import *
import os
import warnings  
warnings.filterwarnings("ignore")  


if __name__ == "__main__":
    #ALTERAR DEPOIS
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
    config = load_config("model/config.json")
    model = config["model"]
    temperature, max_lenght = float(config["temperature"]), int(config["max_lenght"])
    searcher = Model(model, temperature, max_lenght)

    print("Bem vindo ao IntelliSearchAI!")
    while True:
        search = input("Digite sua busca: ")
        anwser = searcher.run(search)
        print("Produtos recomendados: ", anwser)
