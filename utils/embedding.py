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