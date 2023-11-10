import pinecone
import pandas as pd

def processing_bd(df):
    """Processando dados para a inserção no BD vetorial"""
    
    id_list = [df['productId'].values[i] for i in range(len(df))]
    id_list = list(map(str, id_list))
    
    vector_list = [df['embedding_categories'].values[i] for i in range(len(df))]

    metadata_list = []
    for i in range(len(df)):
        metadata_list.append({
            "productName": df["productName"].values[i],
            "brand": df["brand"].values[i],
            #"metaTagDescription": df["metaTagDescription"].values[i],
            "description": df["description"].values[i],
            "categories": df["categories"].values[i],
            "linkText": df["linkText"].values[i],
            "link": df["link"].values[i],
            "filtered_categories": df["filtered_categories"].values[i]
        })
    
    data = [(id_list[i], vector_list[i], metadata_list[i]) for i in range(len(id_list))]

    return data

def vector_db():
    """Chamando instancia"""
    pinecone.init(api_key='0d242db0-0ea7-4fa5-bb1f-161f0d6cf684', environment='gcp-starter')
    index = pinecone.Index('eletronicdata')

    return index

#SSLEOFError tinha dado esse erro logo teve-se que instalar as seguintes libs                             
#pip install ndg-httpsclient
#pip install pyopenssl
#pip install pyasn1

def insert_db(data, index):
    """Inserindo dados no BD"""    
    index.upsert(data)