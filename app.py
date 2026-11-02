import streamlit as st
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
    - Modelo: Mistral (local via Ollama)
    - Documentos: Pasta `data/`
    - Busca semântica: FAISS
    - Execução: 100% offline
    """)

    if st.button("🔄 Recarregar Sistema"):
        if "chain" in st.session_state:
            del st.session_state.chain
        st.rerun()

if "chain" not in st.session_state:
    with st.spinner("Inicializando o assistente..."):
        try:
            st.session_state.chain = criar_chain()
            st.success("Sistema carregado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao inicializar: {str(e)}")
            st.info("""
            **Dicas para resolver:**
            1. Verifique se o Ollama está rodando no terminal (`ollama serve`)
            2. Confirme se o modelo foi baixado (`ollama pull mistral`)
            3. Coloque arquivos PDF ou TXT na pasta `data/`
            """)

st.subheader("Faça sua pergunta sobre os documentos")

with st.form("pergunta_form", clear_on_submit=False):
    pergunta = st.text_input(
        "Digite sua pergunta:",
        placeholder="Ex: O que o documento diz sobre o processo?"
    )
    enviar = st.form_submit_button("Buscar Resposta", type="primary")

if enviar and pergunta:
    if "chain" not in st.session_state:
        st.error("O sistema ainda não foi carregado. Verifique os avisos acima.")
    else:
        with st.spinner("Consultando documentos..."):
            try:
                resultado = st.session_state.chain.invoke({"query": pergunta})
                st.markdown("### Resposta:")
                st.write(resultado["result"])

                with st.expander("Ver trechos consultados"):
                    docs = resultado.get("source_documents", [])
                    if docs:
                        for i, doc in enumerate(docs[:3], 1):
                            fonte = doc.metadata.get("fonte", "Arquivo")
                            pagina = doc.metadata.get("page")
                            info_pag = f" (Pág. {pagina + 1})" if isinstance(pagina, int) else ""
                            st.markdown(f"**Documento {i}:** `{fonte}`{info_pag}")

                            conteudo = doc.page_content.replace("\n", " ").strip()
                            preview = conteudo[:250] + "..." if len(conteudo) > 250 else conteudo
                            st.text(preview)
                            st.markdown("---")
                    else:
                        st.info("Nenhum trecho específico foi recuperado.")
            except Exception as e:
                st.error(f"Erro ao processar a pergunta: {str(e)}")

st.markdown("---")
st.caption("Mini Lum.IA — Executado localmente com Ollama e LangChain.")
