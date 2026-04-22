import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader
import tempfile

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="LaraBot",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Estilos customizados ─────────────────────────────────────────────────────
st.markdown("""
<style>
/* 1. Limpeza total do fundo */
.stApp {
    background-color: #ffffff !important;
}

/* 2. Estilo do Título para fundo claro */
.larabot-title {
    color: #2d2060 !important;
    font-family: 'Fraunces', serif;
    font-size: 3rem;
    font-weight: 700;
}

.larabot-subtitle {
    color: #6b4fa0 !important;
    font-size: 0.8rem;
    opacity: 0.8;
}

/* 3. Balões de Chat (Cores contrastantes) */
.bubble-user {
    background-color: #4B3278 !important; /* Roxo apenas no balão do usuário */
    color: white !important;
    border-radius: 15px;
    padding: 12px 18px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.bubble-bot {
    background-color: #f0f2f6 !important;
    color: #1a1a1a !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 15px;
    padding: 12px 18px;
}

/* 4. Labels (você/larabot) */
.label-user, .label-bot {
    color: #888888 !important;
    font-weight: bold;
    font-size: 0.7rem;
    margin-bottom: 4px;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ─── Inicialização do estado ──────────────────────────────────────────────────
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "documento" not in st.session_state:
    st.session_state.documento = ""
if "fonte_carregada" not in st.session_state:
    st.session_state.fonte_carregada = False
if "fonte_tipo" not in st.session_state:
    st.session_state.fonte_tipo = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = ""


# ─── Funções ──────────────────────────────────────────────────────────────────
def get_chat():
    key = st.session_state.api_key 
    
    if not key:
        st.warning("⬅️ Por favor, insira sua GROQ API Key na barra lateral para começar.")
        return None
        
    return ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=key)


def resposta_bot(mensagens, documento, chat):
    documento_escapado = documento.replace("{", "{{").replace("}", "}}")
    mensagens_modelo = [
        ("system",
         "Você é um assistente amigável chamado LaraBot. "
         "Use as seguintes informações para responder: {documento}")
    ]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({"documento": documento_escapado}).content


def carrega_site(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    return "".join(d.page_content for d in docs)


def carrega_pdf(arquivo):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(arquivo.read())
        tmp_path = tmp.name
    loader = PyPDFLoader(tmp_path)
    docs = loader.load()
    os.unlink(tmp_path)
    return "".join(d.page_content for d in docs)[:8000]


def carrega_youtube(url):
    loader = YoutubeLoader.from_youtube_url(url, language=["pt"])
    docs = loader.load()
    return "".join(d.page_content for d in docs)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## LaraBot")
    st.markdown("Configuração")

    api_input = st.text_input(
        "GROQ API Key",
        type="password",
        placeholder="gsk_...",
        value=st.session_state.api_key
    )
    if api_input:
        st.session_state.api_key = api_input

    st.markdown('<div class="section-tag">Fonte de conhecimento</div>', unsafe_allow_html=True)

    fonte = st.radio(
        "Tipo de fonte",
        ["🌐  Site", "📄  PDF", "▶  YouTube"],
        label_visibility="collapsed"
    )

    if fonte == "🌐  Site":
        url_site = st.text_input("URL do site", placeholder="https://exemplo.com")
        if st.button("Carregar site"):
            with st.spinner("Lendo página..."):
                try:
                    st.session_state.documento = carrega_site(url_site)
                    st.session_state.fonte_carregada = True
                    st.session_state.fonte_tipo = f"🌐 {url_site[:35]}..."
                    st.session_state.mensagens = []
                    st.success("Site carregado!")
                except Exception as e:
                    st.error(f"Erro: {e}")

    elif fonte == "📄  PDF":
        pdf_file = st.file_uploader("Envie o PDF", type=["pdf"])
        if pdf_file and st.button("Carregar PDF"):
            with st.spinner("Extraindo texto..."):
                try:
                    st.session_state.documento = carrega_pdf(pdf_file)
                    st.session_state.fonte_carregada = True
                    st.session_state.fonte_tipo = f"📄 {pdf_file.name}"
                    st.session_state.mensagens = []
                    st.success("PDF carregado!")
                except Exception as e:
                    st.error(f"Erro: {e}")

    elif fonte == "▶  YouTube":
        url_yt = st.text_input("URL do vídeo", placeholder="https://youtube.com/watch?v=...")
        if st.button("Carregar vídeo"):
            with st.spinner("Buscando transcrição..."):
                try:
                    st.session_state.documento = carrega_youtube(url_yt)
                    st.session_state.fonte_carregada = True
                    st.session_state.fonte_tipo = f"▶ {url_yt[:35]}..."
                    st.session_state.mensagens = []
                    st.success("Vídeo carregado!")
                except Exception as e:
                    st.error(f"Erro: {e}")

    st.markdown("---")
    if st.session_state.fonte_carregada:
        st.markdown(
            f'<div class="status-badge">✓ fonte ativa</div><br>'
            f'<span style="font-size:0.72rem;color:#6b6b8a">{st.session_state.fonte_tipo}</span>',
            unsafe_allow_html=True
        )
        chars = len(st.session_state.documento)
        st.caption(f"{chars:,} caracteres indexados")
    else:
        st.markdown('<div class="status-badge status-badge-warn">⊘ sem fonte</div>', unsafe_allow_html=True)

    if st.session_state.mensagens:
        if st.button("🗑  Limpar conversa"):
            st.session_state.mensagens = []
            st.rerun()


# ─── Área principal ───────────────────────────────────────────────────────────
col_title, _ = st.columns([3, 1])
with col_title:
    st.markdown('<div class="larabot-title">LaraBot</div>', unsafe_allow_html=True)
    st.markdown('<div class="larabot-subtitle">Assistente de documentos, sites e vídeos · powered by llama 3.3</div>', unsafe_allow_html=True)

# Estado vazio
if not st.session_state.fonte_carregada:
    st.markdown("""
    <div style="margin-top:3rem; padding:2rem; border:1px dashed #2a2a45; border-radius:16px; text-align:center;">
        <div style="font-size:2rem; margin-bottom:0.8rem;">✦</div>
        <div style="font-family:'Fraunces',serif; font-size:1.3rem; color:#c8b8f0; margin-bottom:0.5rem;">
            Carregue uma fonte para começar
        </div>
        <div style="font-size:0.78rem; color:#4a4a6a; line-height:1.8;">
            Selecione um site, PDF ou vídeo do YouTube na barra lateral.<br>
            O LaraBot irá ler o conteúdo e responder suas perguntas sobre ele.
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Histórico de mensagens
    chat_html = '<div class="chat-wrap">'
    for role, texto in st.session_state.mensagens:
        if role == "user":
            chat_html += f"""
            <div class="msg-user">
                <div>
                    <div class="label-user">você</div>
                    <div class="bubble-user">{texto}</div>
                </div>
            </div>"""
        else:
            chat_html += f"""
            <div class="msg-bot">
                <div>
                    <div class="label-bot">larabot</div>
                    <div class="bubble-bot">{texto}</div>
                </div>
            </div>"""
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # Input do usuário
    st.markdown('<div class="section-tag">Qual é a sua pergunta?</div>', unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            pergunta = st.text_input(
                "Pergunta",
                placeholder="O que você quer saber sobre esse conteúdo?",
                label_visibility="collapsed"
            )
        with col_btn:
            enviar = st.form_submit_button("Enviar →")

    if enviar and pergunta.strip():
        chat = get_chat()
        if chat:
            st.session_state.mensagens.append(("user", pergunta))
            with st.spinner("LaraBot está pensando..."):
                try:
                    resposta = resposta_bot(st.session_state.mensagens, st.session_state.documento, chat)
                    st.session_state.mensagens.append(("assistant", resposta))
                except Exception as e:
                    st.error(f"Erro ao gerar resposta: {e}")
                    st.session_state.mensagens.pop()
            st.rerun()
