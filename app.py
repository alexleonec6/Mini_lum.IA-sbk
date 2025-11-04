import streamlit as st
# Garante que a importação do engine está correta
from chat_engine import criar_chain

st.set_page_config(
    page_title="Mini Lum.IA - SBK",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Mini Lum.IA - Assistente SBK")
st.markdown("**Chat de IA local que responde perguntas sobre documentos internos**")
st.markdown("---")

with st.sidebar:
    st.header("📊 Status do Sistema")
    st.markdown("""
    **Configuração:**
    - 🤖 Modelo: Mistral (local, via Ollama)
    - 📚 Documentos: Pasta (data)
    - 🔍 Busca semântica (FAISS)
    - 🌐 Totalmente offline
    """)

    if st.button("🔄 Recarregar Sistema"):
        # Limpa o cache e força a recriação da chain
        if "chain" in st.session_state:
            del st.session_state.chain
        st.rerun()

if "chain" not in st.session_state:
    with st.spinner("🚀 Inicializando sistema IA... Isso pode levar alguns segundos (dependendo do tamanho dos documentos)."):
        try:
            # Tenta criar e carregar a chain RAG
            st.session_state.chain = criar_chain()
            st.success("✅ Sistema carregado com sucesso!")
        except Exception as e:
            # Exibe erro e dicas de solução de problemas
            st.error(f"❌ Erro de inicialização: {str(e)}")
            st.info("""
            **Para resolver:**
            1. Verifique se o **Ollama está rodando** em outro terminal: `ollama serve`
            2. Confirme se o **modelo Mistral está instalado**: `ollama pull mistral`
            3. Verifique se a **pasta 'data'** existe e contém arquivos PDF ou TXT.
            """)

st.subheader("💬 Faça sua pergunta sobre os documentos")

pergunta = st.text_input(
    "Digite sua pergunta:",
    placeholder="Ex: Quais são as políticas de férias? O que diz o documento X sobre o processo Y?"
)

if st.button("🔍 Buscar Resposta", type="primary") and pergunta:
    if "chain" not in st.session_state:
        st.error("Sistema não carregado. Verifique a seção de status acima.")
    else:
        with st.spinner("🔍 Consultando documentos e gerando resposta..."):
            try:
                # Usa .invoke() para LangChain 0.1.x
                resultado = st.session_state.chain.invoke({"query": pergunta}) 
                st.markdown("### 🧠 Resposta:")
                st.write(resultado["result"])

                with st.expander("📚 Ver documentos consultados"):
                    if resultado.get("source_documents"):
                        st.markdown("Estes são os trechos que a IA utilizou como contexto:")
                        for i, doc in enumerate(resultado["source_documents"][:3], 1):
                            fonte = doc.metadata.get("fonte", "N/A")
                            # Usa get('page', 'N/A') se estiver usando PyPDFLoader
                            pagina = doc.metadata.get('page', 'N/A')
                            st.markdown(f"**Documento {i}:** {fonte} (Pág: {pagina})") 
                            
                            # Limita o tamanho do preview
                            conteudo = doc.page_content.replace('\n', ' ')
                            conteudo_preview = conteudo[:250] + "..." if len(conteudo) > 250 else conteudo
                            st.text(conteudo_preview)
                            st.markdown("---")
                    else:
                        st.info("Nenhum documento específico foi consultado (a resposta pode ser conhecimento geral do modelo).")
            except Exception as e:
                st.error(f"Erro ao processar a consulta. Verifique o console para mais detalhes. Erro: {str(e)}")

st.markdown("---")
st.markdown("💡 **Dica:** Faça perguntas específicas sobre o conteúdo dos documentos para melhores respostas. Lembre-se de que o **Ollama deve estar ativo** para que o sistema funcione.")
