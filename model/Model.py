from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.Cleaner import answer_cleaner
from utils.Logger import save_log

"""
Documetação da classe Model:
    Atributos:
        model_name: Nome do modelo a ser utilizado.
        prompt_template: Template do prompt a ser utilizado.
        temperature: Temperatura a ser utilizada no modelo.
        max_lenght: Tamanho máximo da resposta a ser gerada pelo modelo.
        
    Métodos:
        run: Método responsável por rodar o modelo.
        retorno:
            Resposta gerada pelo modelo.
"""

class Model():
    def __init__(self, model_name, temperature, max_lenght):
        self.PROMPT_TEMPLATE = """Com base nas informações fornecidas na busca do usuário, recomende uma lista de produtos que atendam às suas necessidades,
        incluindo nome e especificações do item. Se você não souber a resposta, apenas diga que não sabe, não tente inventar uma resposta.
        exemplo 1:
        Pergunta: Itens para montar um setup
        Resposta: Monitor, Computador, Teclado, Mouse

        exemplo 2:
        Pergunta: Preciso decorar meu banheiro
        Resposta: Toalha, Saboneteira, Porta papel higiênico

        {pergunta}"""

        self.prompt = PromptTemplate(template=self.PROMPT_TEMPLATE, input_variables=["pergunta"])
        self.llm = HuggingFaceHub(repo_id=model_name,
                                    model_kwargs={"temperature": temperature, "max_length": max_lenght})

        self.llm_chain = LLMChain(prompt=self.prompt, llm=self.llm)
    
    def run(self, input):
        answer = self.llm_chain.run(input)
        clean_answer = answer_cleaner(answer)
        save_log(input, clean_answer)
        return clean_answer