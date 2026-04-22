import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY não encontrada no .env")

chat = ChatGroq(
    model='llama-3.3-70b-versatile',
    groq_api_key=api_key
)


def resposta_bot(mensagens, documento):
    documento_escapado = documento.replace('{', '{{').replace('}', '}}')
    mensagens_modelo = [
        ('system', 'Você é um assistente amigável chamado LaraBot. '
                   'Use as seguintes informações para responder: {documento}')
    ]
    mensagens_modelo += mensagens

    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat

    return chain.invoke({'documento': documento_escapado}).content


def carrega_site():
    url_site = input('Digite a url do site: ')
    loader = WebBaseLoader(url_site)
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento


def carrega_pdf():
    caminho = input('Digite o caminho do arquivo PDF: ')
    loader = PyPDFLoader(caminho)
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento[:8000] 

def carrega_youtube():
    url_youtube = input('Digite a url do vídeo: ')
    loader = YoutubeLoader.from_youtube_url(url_youtube, language=['pt'])
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento


print("Bem-vindo ao LaraBot")
print("Caso queira sair, digite 'x'")

texto_selecao = '''
Digite 1 se você quiser conversar com um site
Digite 2 se você quiser conversar com um PDF
Digite 3 se você quiser conversar com um vídeo do YouTube
'''

while True:
    selecao = input(texto_selecao)
    if selecao == '1':
        documento = carrega_site()
        break
    if selecao == '2':
        documento = carrega_pdf()
        break
    if selecao == '3':
        documento = carrega_youtube()
        break
    print('Digite um valor entre 1 e 3')

mensagens = []
while True:
    pergunta = input('Usuário: ')
    if pergunta.lower() == 'x':
        break
    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens, documento)
    mensagens.append(('assistant', resposta))
    print(f'Bot: {resposta}')

print('Muito obrigado por me utilizar!')