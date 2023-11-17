import json
from unidecode import unidecode
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st  
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stopwords = set(stopwords.words('portuguese'))

def word_cloud():
    with open('log/log.json', encoding='utf-8') as file:
        logs = json.load(file)

    all_text = []
    for log in logs:
        all_text.extend(log['Respostas'])

    all_text_str = ' '.join(all_text)
    #Remove acentos
    all_text_str = unidecode(all_text_str)
    #Remove stopwords
    all_text_str = ' '.join([word for word in all_text_str.split() if word not in stopwords])

    icon = Image.open("utils/cloud.png")
    image_mask = Image.new(mode='RGB', size=icon.size, color=(255,255,255))
    image_mask.paste(icon, box=icon)

    rgb_array = np.array(image_mask) 

    word_cloud = WordCloud(mask=rgb_array, background_color='white', max_font_size=500,
                           max_words=500, colormap='gist_heat')
    word_cloud.generate(all_text_str.upper())

    fig, ax = plt.subplots(figsize=[40,20])
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis('off')
    st.pyplot(fig)