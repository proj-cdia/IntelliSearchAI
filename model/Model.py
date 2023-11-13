from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.answer_cleaner import answer_cleaner
from utils.log_saver import save_log

"""
Documetação da classe Model:
    Atributos:
        model_name: Nome do modelo a ser utilizado.
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
        self.PROMPT_TEMPLATE2 = """Com base nas informações fornecidas na busca do usuário, recomende uma lista com nomes de produtos que mais estejam relacionados com o contexto fornecido.
        Não complete a entrada do usuário, somente relacione a frase de entrada com produtos interessantes no contexto.
        Caso seja informado, considere características específicas como cores e tamanhos para acertar a resposta, conforme o exmplo 3.
        Se você não souber a resposta, apenas diga que não sabe, não tente inventar uma resposta.

        exemplo 1:
        Pergunta: Quero comprar móveis para sala de estar
        Resposta: Sofá, Televisão, Tapete, Mesa de Jantar

        exemplo 2:
        Pergunta: Preciso decorar meu banheiro
        Resposta: Toalha, Saboneteira, Porta papel higiênico

        exemplo 3:
        Pergunta: Quero cobertas verdes
        Resposta: Lençol verde, fronhas verdes, cobertor verde, colcha verde

        {pergunta}"""

        self.prompt = PromptTemplate(template=self.PROMPT_TEMPLATE, input_variables=["pergunta"])
        self.prompt2 = PromptTemplate(template=self.PROMPT_TEMPLATE2, input_variables=["pergunta"])

        self.llm = HuggingFaceHub(repo_id=model_name,
                                    model_kwargs={"temperature": temperature, "max_length": max_lenght})

        self.llm_chain = LLMChain(prompt=self.prompt, llm=self.llm)
        self.llm_chain2 = LLMChain(prompt=self.prompt2, llm=self.llm)
    
    def run(self, input):
        answer = self.llm_chain.run(input)
        answer2 = self.llm_chain2.run(input)
        clean_answer = answer_cleaner(answer)
        clean_answer2 = answer_cleaner(answer2)
        result = list(set(clean_answer + clean_answer2))
        result_sorted = sorted(result)
        result_string = ', '.join(result_sorted)
        save_log(input, result)
        return result_string