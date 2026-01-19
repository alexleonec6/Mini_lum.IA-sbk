Mini-lum.IA: Assistente RAG (Retrieval-Augmented Generation) Local

Este projeto implementa um sistema de Q&A (Perguntas e Respostas) baseado na arquitetura RAG (Retrieval-Augmented Generation). Ele permite que a inteligência artificial responda perguntas complexas consultando exclusivamente uma base de conhecimento privada (seus próprios documentos). A solução é construída para operar de forma totalmente local e privada, garantindo total controle sobre os dados e o LLM.

Destaques do Projeto

Arquitetura RAG Completa: Implementação de um pipeline robusto que inclui carregamento de documentos, chunking, criação de embeddings e busca por similaridade semântica.

Modelo Open Source: Utiliza o Ollama como servidor de LLM e o modelo Mistral para geração de respostas.

Privacidade e Autonomia: Toda a operação é realizada na máquina local, sem dependência de APIs externas ou envio de dados sensíveis para a nuvem.

Interface Amigável: Desenvolvido com Streamlit para uma interface de chat interativa e fácil de usar.

Tecnologias Utilizadas

Categoria

Tecnologia

Uso no Projeto

Orquestração RAG

LangChain

Framework principal para conectar todos os componentes e gerenciar o fluxo do chat.

Servidor LLM

Ollama

Responsável por executar o LLM Mistral localmente.

LLM (Geração)

Mistral

Modelo de código aberto utilizado para criar embeddings e gerar as respostas finais.

Banco Vetorial

FAISS

Usado para armazenar vetores e realizar buscas por similaridade semântica de alta performance.

Interface Web

Streamlit

Criação da interface de usuário e da lógica de sessão do chat.

Instalação e Configuração

1. Pré-requisitos

Certifique-se de ter o Python (3.10+) e o Git instalados.

2. Ollama (Servidor LLM)

Você deve ter o Ollama instalado e rodando em sua máquina.

Instalar o Ollama: Baixe e instale a versão para o seu sistema operacional.

Baixar o Modelo Mistral: Abra um terminal e execute:

ollama pull mistral


Iniciar o Servidor: Mantenha o servidor Ollama rodando em um terminal (ou em segundo plano):

ollama serve


3. Configuração do Projeto Python

Clone o Repositório:

git clone [https://github.com/alexleonec6/Mini_lum.IA-sbk.git](https://github.com/alexleonec6/Mini_lum.IA-sbk.git)
cd Mini_lum.IA-sbk


Criar e Ativar o Ambiente Virtual:

python -m venv venv
.\venv\Scripts\activate  # No Windows
# source venv/bin/activate  # No Linux/macOS


Instalar Dependências:

pip install -r requirements.txt


Uso

1. Adicionar Documentos

Coloque todos os seus arquivos de conhecimento (.pdf, .txt, etc.) dentro da pasta data/ na raiz do projeto.

2. Iniciar o Assistente

Com o Ollama rodando e o ambiente virtual ativado, inicie o Streamlit:

streamlit run app.py


O aplicativo será aberto automaticamente no seu navegador. A primeira execução irá processar e vetorizar seus documentos, criando a base FAISS no disco (o que pode levar alguns minutos, dependendo do volume de dados).

Estrutura do Projeto

Mini_lum.IA-sbk/
├── data/                       
├── venv/                       
├── .gitignore                  
├── requirements.txt            
├── app.py                      
└── chat_engine.py           
