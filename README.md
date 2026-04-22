# ✦ LaraBot

Assistente inteligente que permite conversar com conteúdos externos utilizando IA.

O LaraBot lê informações de diferentes fontes e responde perguntas de forma contextual, utilizando modelos de linguagem avançados via Groq + LangChain.

---

## 🚀 Funcionalidades

* 🌐 Leitura e interpretação de sites
* 📄 Extração de texto de arquivos PDF
* ▶️ Transcrição e análise de vídeos do YouTube
* 💬 Chat contextual com memória de conversa
* 🖥️ Interface em terminal (CLI)
* 🌐 Interface web interativa com Streamlit

---

## 🧠 Tecnologias utilizadas

* Python
* LangChain
* Groq API (LLM - Llama 3.3)
* Streamlit
* BeautifulSoup
* PyPDF
* YouTube Transcript API

---

## 📁 Estrutura do projeto

```
larabot/
│
├── cli.py              # Versão em terminal
├── app.py              # Interface com Streamlit
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Como executar o projeto

### 1. Clonar o repositório

```
git clone https://github.com/LaraAlves22/LaraBot.git
cd LaraBot
```

---

### 2. Criar ambiente virtual

**Windows:**

```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Instalar dependências

```
pip install -r requirements.txt
```

---

### 4. Configurar variável de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
GROQ_API_KEY=sua_chave_aqui
```

---

## ▶️ Executando

### 💻 Versão terminal (CLI)

```
python cli.py
```

---

### 🌐 Versão web (Streamlit)

```
streamlit run app.py
```

---

## 💡 Exemplos de uso

* Perguntar sobre o conteúdo de um artigo online
* Analisar um PDF acadêmico
* Fazer perguntas sobre um vídeo do YouTube
* Resumir conteúdos extensos

---

## 🔐 Segurança

O projeto utiliza variáveis de ambiente para proteger a chave da API.
O arquivo `.env` não deve ser versionado (já incluído no `.gitignore`).

---

## 📌 Possíveis melhorias

* Implementar armazenamento de histórico
* Melhorar UI/UX da interface Streamlit
* Adicionar suporte a múltiplos documentos simultâneos
* Deploy em nuvem (Streamlit Cloud ou Render)

---

## ⭐ Observação

Este projeto foi desenvolvido com foco em aprendizado prático de integração com modelos de linguagem e construção de aplicações de IA.
