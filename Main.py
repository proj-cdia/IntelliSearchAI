import pandas as pd  
import json
import os  
import warnings    
import streamlit as st  
from data_processing import pre_processing, vector_db  
from utils.config_loader import load_config  
from model.Model import Model
from utils.embedding import embedding  
  
warnings.filterwarnings("ignore")    
  
def main():  
    # Carrega as configurações do modelo    
    os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'  
    config = load_config("model/config.json")    
    model = config["model"]    
    temperature, max_lenght = float(config["temperature"]), int(config["max_lenght"])    
    searcher = Model(model, temperature, max_lenght)  
  
    # Instancia o banco de dados  
    index = vector_db.vector_db()  
  
    # Sidebar para carregar os dados  
    st.sidebar.title("Carregar Datasets")  
    st.sidebar.markdown('Selecione o arquivo JSON para carregar:')  
    uploaded_file = st.sidebar.file_uploader("", type="json")    
      
    if uploaded_file is not None:    
        data = pd.read_json(uploaded_file)    
        st.sidebar.write('Pré-visualização dos dados:')  
        st.sidebar.dataframe(data.head())    
      
        if st.sidebar.button('Carregar dataset'):    
            with st.spinner('Carregando e processando dados...'):  
                produto = pre_processing.format_data('data\Products')    
                df = pre_processing.processing_df(produto)    
                df = pre_processing.processing_and_embed(df)    
                pre_processing.new_file(df)    
      
                # Carregando e inserindo os dados no BD    
                df = pd.read_csv('Products.csv')    
                data = vector_db.processing_bd(df)      
                vector_db.insert_db(data, index)    
            st.sidebar.success("Dataset carregado e processado com sucesso!")    
  
    # Cria a interface do Streamlit    
    st.title("IntelliSearchAI")    
    st.markdown('Bem vindo ao IntelliSearchAI! Digite sua busca abaixo:')    
    # Campo de busca e botão de pesquisar    
    search = st.text_input("")    
    if st.button('Pesquisar'):    
        with st.spinner('Pesquisando...'):  
            models_answer = searcher.run(search)   
            models_answer = sorted(list(set([item.strip().upper() for item in models_answer.split(",") if len(item)>1])))
            models_answer = " , ".join(models_answer)
            if len(models_answer) > 0:
                st.subheader("Resposta do Modelo: ")  
                st.write(models_answer)  
                embedding_anwser = embedding(models_answer)  
                pinecone_anwser = vector_db.query_db(index, embedding_anwser)

                # Processamento da consulta(pinecone_anwser)
                filtered_data = []
                for match in pinecone_anwser["matches"]:
                    filtered_data.append({
                        "id": match["id"],
                        "score": match["score"],
                        "brand": match["metadata"]["brand"],
                        "link": match["metadata"]["link"],
                        "productName": match["metadata"]["productName"]
                    })

                st.subheader("Produtos recomendados: ")  

                for item in filtered_data:
                    st.write("--------------------------------")
                    st.write(f"Nome do Produto: {item['productName']}")
                    st.write(f"ID: {item['id']}")
                    st.write(f"Score: {item['score']}")
                    st.write(f"Marca: {item['brand']}")
                    st.write(f"Link: {item['link']}")
            else:
                st.write("Nenhum produto encontrado! Tente novamente.")
  
if __name__ == "__main__":  
    main()