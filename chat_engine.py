import os
import requests
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

def verificar_ollama():
    # checa se o ollama tá rodando localmente
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def carregar_docs():
    pasta = "data"
    docs = []

    if not os.path.exists(pasta):
        os.makedirs(pasta)

    arquivos = [f for f in os.listdir(pasta) if f.endswith((".pdf", ".txt"))]

    # se não tiver nenhum arquivo, cria um exemplo básico pra não quebrar a aplicação
    if not arquivos:
        exemplo_path = os.path.join(pasta, "exemplo.txt")
        with open(exemplo_path, "w", encoding="utf-8") as f:
            f.write(
                "Mini Lum.IA - Assistente RAG Local\n\n"
                "Este é um documento de teste inicial do sistema.\n"
                "Para fazer perguntas sobre seus documentos, coloque seus arquivos PDF ou TXT dentro da pasta 'data' "
                "e recarregue o assistente pelo menu lateral."
            )
        arquivos = ["exemplo.txt"]

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        try:
            if arquivo.endswith(".pdf"):
                loader = PyPDFLoader(caminho)
                carregados = loader.load()
            elif arquivo.endswith(".txt"):
                loader = TextLoader(caminho, encoding="utf-8")
                carregados = loader.load()
            else:
                continue

            for doc in carregados:
                doc.metadata["fonte"] = arquivo
            docs.extend(carregados)
        except Exception as e:
            print(f"Erro ao carregar o arquivo {arquivo}: {e}")

    return docs

def criar_chain():
    # 1. verifica se o serviço do ollama tá ativo
    if not verificar_ollama():
        raise Exception("Ollama não está rodando. Inicie com 'ollama serve' no terminal.")

    # 2. carrega os documentos da pasta data
    docs = carregar_docs()
    if not docs:
        raise Exception("Nenhum documento encontrado na pasta 'data'. Adicione arquivos PDF ou TXT.")

    # 3. divide os textos em chunks menores pra caber no modelo
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    # 4. gera os embeddings e o índice vetorial no faiss
    embeddings = OllamaEmbeddings(model="mistral")
    db = FAISS.from_documents(chunks, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # 5. conecta no modelo mistral e cria a chain de QA
    llm = Ollama(model="mistral", temperature=0.1)
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    return chain

if __name__ == "__main__":
    try:
        print("Iniciando teste da chain...")
        chain = criar_chain()
        print("Chain criada com sucesso!")
    except Exception as e:
        print(f"Erro no teste: {e}")
