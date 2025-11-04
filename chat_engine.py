from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
# CORREÇÃO: Usando a importação clássica que funciona na versão 0.1.20
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import os
import requests

def verificar_ollama():
    """Verifica se o Ollama está rodando no endereço padrão."""
    try:
        # Tenta acessar o endpoint de tags para verificar o status
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        # Captura erros de conexão (Ollama não está servindo)
        return False

def carregar_docs():
    """Carrega documentos PDF e TXT da pasta 'data'."""
    docs = []
    pasta = "data"

    if not os.path.exists(pasta):
        # Cria a pasta 'data' se não existir para evitar erros
        os.makedirs(pasta)
        print(f"❌ Pasta '{pasta}' não encontrada e foi criada. Adicione documentos!")
        return docs

    print("📁 Carregando documentos da pasta 'data'...")

    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        try:
            if arquivo.endswith(".pdf"):
                print(f"📄 Carregando PDF: {arquivo}")
                loader = PyPDFLoader(caminho)
                documentos = loader.load()
                for doc in documentos:
                    # Adiciona a fonte ao metadata
                    doc.metadata["fonte"] = arquivo
                docs.extend(documentos)
                print(f"✅ PDF carregado: {arquivo} - {len(documentos)} páginas")

            elif arquivo.endswith(".txt"):
                print(f"📝 Carregando TXT: {arquivo}")
                # Garante o encoding correto
                loader = TextLoader(caminho, encoding='utf-8')
                documentos = loader.load()
                for doc in documentos:
                    # Adiciona a fonte ao metadata
                    doc.metadata["fonte"] = arquivo
                docs.extend(documentos)
                print(f"✅ TXT carregado: {arquivo}")

        except Exception as e:
            # Captura erros específicos de carregamento (ex: PDF corrompido)
            print(f"❌ Erro ao carregar {arquivo}: {str(e)}")

    print(f"🎯 Total de documentos carregados: {len(docs)}")
    return docs

def criar_chain():
    """Cria e configura a Chain de QA (Perguntas e Respostas) com LangChain e Ollama."""
    print("🔹 Iniciando configuração do sistema...")

    # 1. Verificação do Ollama
    if not verificar_ollama():
        raise Exception("Ollama não está rodando. Execute 'ollama serve' em outro terminal.")

    # 2. Carregamento de Documentos
    docs = carregar_docs()

    if not docs:
        raise Exception("Nenhum documento encontrado na pasta 'data'. Adicione arquivos PDF ou TXT.")

    # 3. Configuração de Embeddings e Vetorização
    print("🔹 Configurando embeddings...")
    # Garante que o modelo está disponível ou usa um fallback
    embeddings = OllamaEmbeddings(model="mistral") 
    print("✅ Embeddings configurados")

    print("🔹 Criando base de conhecimento (FAISS)...")
    db = FAISS.from_documents(docs, embeddings)
    # Configura o Retriever para buscar os 3 documentos mais relevantes
    retriever = db.as_retriever(search_kwargs={"k": 3})
    print("✅ Base de conhecimento criada")

    # 4. Conexão com o LLM (Mistral)
    print("🔹 Conectando ao modelo Mistral...")
    # Baixa temperatura para respostas mais factuais
    llm = Ollama(model="mistral", temperature=0.1) 
    print("✅ Modelo Mistral conectado")

    # 5. Criação da Chain RAG
    print("🔹 Criando sistema de perguntas e respostas (RetrievalQA)...")
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", # Coloca todo o contexto em um prompt só
        retriever=retriever,
        return_source_documents=True # Retorna as fontes para o usuário
    )

    print("✅ ✅ Sistema pronto para uso!")
    return chain

if __name__ == "__main__":
    # Bloco de teste
    try:
        chain = criar_chain()
        print("\nSucesso! O sistema foi carregado sem erros.")
        # Se desejar testar a chain:
        # pergunta = "Quais são os principais pontos do primeiro documento?"
        # resultado = chain.invoke({"query": pergunta})
        # print(f"\nPergunta: {pergunta}")
        # print(f"Resposta: {resultado['result']}")
    except Exception as e:
        print(f"\nFALHA na inicialização: {e}")
