import pandas as pd
import json
import os
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
from retry import retry
import requests

@retry(tries=3, delay=10)
def embedding(texts):
    # ALTERAR DEPOIS PARA NAO SER HARD CODED
    hf_token = "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"

    # Embedding baseado no código do link abaixo
    # https://colab.research.google.com/github/huggingface/blog/blob/main/notebooks/80_getting_started_with_embeddings.ipynb#scrollTo=Kg0HaYGSz2GC
    model = 'sentence-transformers/all-mpnet-base-v2' # DIM 768
    #model = 'sentence-transformers/all-MiniLM-L6-v2' # DIM 348
    model_id = model

    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
    headers = {"Authorization": f"Bearer {hf_token}"}


    response = requests.post(api_url, headers=headers, json={"inputs": texts})
    result = response.json()
    if isinstance(result, list):
      return result
    elif list(result.keys())[0] == "error":
      raise RuntimeError(
          "The model is currently loading, please re-run the query."
          ) 


def clean_html(html):
    """Formata o HTML recebido e retorna somente o texto"""
    return BeautifulSoup(html, "html.parser").text

def refine_category(categories:list) -> list:
    """Dado o padrão com que as categorias são recebidas, retorna uma lista com os elementos exclusivos contidos nas categorias"""
    elements = []
    for cat in categories:
        c = cat.split("/")
        for element in c:
            if element != "":
                elements.append(element)
    elements = list(set(elements))
    elements = [unidecode(element.upper()) for element in elements]
    return elements

def norm_text(text:str) -> str:
    """Normaliza o texto retirando acentuação e colocando totalmente em letras maiúsculas"""
    return unidecode(text).upper()

def format_data(path):
    """Formata os dados do json para um df"""
    produtos = pd.DataFrame()
    json_file_names = [filename for filename in os.listdir(f"{path}") if filename.endswith('.json')]

    for json_file in json_file_names:
        produtos = pd.concat([produtos,pd.read_json(rf"{path}/{json_file}")]).reset_index(drop=True)

    return produtos

def processing_df(prod):
    """Processamento das colunas e filtragem das categorias"""
    colunas = ["productId","productName","brand","metaTagDescription","description","categories","linkText","link"]
    df = prod[colunas]

    df["description"] = df["description"].apply(clean_html)
    df["description"] = df["description"].str.replace("\n","")
    df["description"] = df["description"].str.replace("\r","")
    # df["description"] = df["description"].apply(normText)

    df["filtered_categories"] = df["categories"].apply(refine_category)

    return df
 
    
def processing_and_embed(df):
    """Processamento e embedding dos dados"""
    # Ordernação das categorias em ordem alfabetica
    df['filtered_categories'] = df['filtered_categories'].apply(lambda x: sorted(x))
    # Lista para string
    df['filtered_categories'] = df['filtered_categories'].apply(lambda x: ', '.join(x[0:3]))
    # Embedding
    df['embedding_categories'] = df['filtered_categories'].apply(lambda x: (embedding(x)))
    # String para lista
    #df['embedding_categories'] = df['embedding_categories'].apply(lambda x: (eval(x)))
    return df

def new_file(df):
    path = path = 'data\processed-data'
    df.to_csv(f'{path}/Products.csv', index=False)
