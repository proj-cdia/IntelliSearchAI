import pandas as pd
import os
import warnings  
from data_processing import pre_processing, vector_db
from utils.config_loader import load_config
from model.Model import *

warnings.filterwarnings("ignore")  


if __name__ == "__main__":
    # ALTERAR DEPOIS PARA NAO SER HARD CODED
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

    # Carregando, processando e fazendo os embedding dos dados
    produto = pre_processing.format_data('data\Products')
    print(type(produto[1]))
    df = pre_processing.processing_df(produto)
    df = pre_processing.processing_and_embed(df)
    pre_processing.new_file(df)

    # Carregando e inserindo os dados no BD
    # df = pd.read_csv('Products.csv')
    # data = vector_db.processing_bd(df)
    # index = vector_db.vector_db()
    # vector_db.insert_db(data, index)

    # Carregando e executando o modelo
    config = load_config("model/config.json")
    model = config["model"]
    temperature, max_lenght = float(config["temperature"]), int(config["max_lenght"])
    searcher = Model(model, temperature, max_lenght)

    print("Bem vindo ao IntelliSearchAI!")
    while True:
        search = input("Digite sua busca: ")
        anwser = searcher.run(search)
        print("Produtos recomendados: ", anwser)
