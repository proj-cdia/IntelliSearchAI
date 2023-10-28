# IntelliSearchAI

COLOCAR DESCRIÇÃO BONITA DO PROJETO E SUAS FUNCIONALIDADES

## Requisitos

- Python 3.8 ou superior
- Uma conta no HuggingFace e uma chave da API. Crie uma conta aqui:<br>
  https://huggingface.co/welcome
- Um token de acesso pessoal HuggingFace. Obtenha um aqui:<br>
  https://huggingface.co/settings/tokens

## Configuração

1. Clone este repositório.
2. Dentro da pasta do projeto, instale as dependências do projeto com:

```
pip install -r requirements.txt

```

3. Crie um novo arquivo .env na raiz do projeto.
4. Adicione suas chaves ao arquivo .env como:

```
HUGGINGFACEHUB_API_TOKEN="SEU_TOKEN_HUGGINGFACE"
```

5. Caso queira alterar as configurações do modelo de Large Language Model, no arquivo config.json dentro da pasta model, adicione o nome do seu modelo, a temperatura e o comprimento máximo desejado para a geração de respostas.

## Uso:

Execute o script com:

```
python main.py
```
