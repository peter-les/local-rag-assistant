# app.py
import sys
from pathlib import Path

# Pridanie src priečinka do cesty, aby fungovali importy
sys.path.append(str(Path(__file__).parent / "src"))

import streamlit as st
from PIL import Image

from rag import ask
from search_filter import SearchFilter
from vector_store import (
    get_all_authors,
    get_all_books
)
from conversation import Conversation  # <- Import presunutý sem nahor
from config import VERSION

# Nastavenie konfigurácie stránky
st.set_page_config(
    page_title="WisdomRAG",
    page_icon="📚",
    layout="wide"
)

# === AGRESÍVNE ZMENŠENIE MEDZIER V SIDEBARE ===
st.markdown(
    """
    <style>
    /* 1. Úplné vynulovanie vrchného okraja pre hlavný kontajner sidebaru */
    [data-testid="stSidebarContent"] {
        padding-top: 0px !important;
    }
    
    /* 2. Vynulovanie vrchného okraja pre používateľský obsah */
    [data-testid="stSidebarUserContent"] {
        padding-top: 10px !important; /* Minimum na estetickú rezervu */
        padding-bottom: 5px !important;
    }

    /* 3. Zrušenie dedičného paddingu na starších verziách Streamlitu */
    [data-testid="stSidebar"] section {
        padding-top: 0px !important;
    }
    
    /* 4. Extrémne zmenšenie rozostupov medzi jednotlivými prvkami */
    [data-testid="stSidebar"] .element-container {
        margin-bottom: 4px !important;
    }
    
    /* 5. Odstránenie horného a dolného okraja nadpisov */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        margin-top: 2px !important;
        margin-bottom: 2px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    
    /* 6. Zmrštenie oddeľovacích čiar (dividerov) */
    [data-testid="stSidebar"] hr {
        margin-top: 6px !important;
        margin-bottom: 6px !important;
    }
    
    /* 7. Zmenšenie veľkosti a paddingu pre info box (Top K) */
    [data-testid="stSidebar"] [data-testid="stNotification"] {
        padding: 4px 10px !important;
        margin-top: 2px !important;
        margin-bottom: 2px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Logo a hlavný nadpis (vedľa seba) ----------------
col_logo, col_title = st.columns([2, 15], vertical_alignment="center")

with col_logo:
    try:
        logo = Image.open("assets/logo.png")
        st.image(logo, width=90)
    except FileNotFoundError:
        st.markdown("# 🍃")

with col_title:
    st.title("WisdomRAG", anchor=False)
    st.caption("A local AI assistant powered entirely by your own books.")

# Inicializácia session state (pamäte aplikácie)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    st.session_state.conversation = Conversation()

if "filter" not in st.session_state:
    st.session_state.filter = SearchFilter()
    
# ---------------- Sidebar (Bočný panel) ----------------
st.sidebar.title("Settings")
st.sidebar.subheader("Knowledge Base")

# Výber autorov
authors = get_all_authors()
selected_authors = st.sidebar.multiselect(
    "Authors",
    authors,
    default=authors
)

# Výber kníh
books = get_all_books()
selected_books = st.sidebar.multiselect(
    "Books",
    books,
    default=books
)

# Nastavenie filtrov na základe výberu
current_filter = SearchFilter()

if len(selected_authors) != len(authors):
    current_filter.authors = selected_authors

if len(selected_books) != len(books):
    current_filter.books = selected_books

st.sidebar.divider()
st.sidebar.subheader("Retrieval")
from config import TOP_K
st.sidebar.info(
    f"""
Top K: {TOP_K}
"""
)
st.sidebar.divider()

# Tlačidlo na vymazanie histórie
if st.sidebar.button("🗑 Clear conversation"):
    st.session_state.messages = []
    st.session_state.conversation.clear()  # <-- OPRAVENÉ: Vyčistíme aj objekt histórie pre LLM a retriever!
    st.rerun()
    
st.sidebar.divider()
st.sidebar.caption(f"WisdomRAG v{VERSION}")


# ---------------- KROK 4 – Úvodná obrazovka ----------------
if len(st.session_state.messages) == 0:
    st.info(
        """
        👋 Welcome to WisdomRAG.

        This assistant answers questions exclusively from your selected books.

        Example questions:
        • What is love?
        • What is ego?
        • What is awareness?
        • What is meditation?
        """
    )

# ---------------- Zobrazenie histórie konverzácie ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "citations" in message and message["citations"]:
            with st.expander("📚 Sources"):
                st.markdown(message["citations"])
        
# ---------------- Četové vstupné pole ----------------
question = st.chat_input("Ask a question...")

# ---------------- Reakcia na novú otázku ----------------
if question:
    # 1. Pridanie otázky do pamäte a jej okamžité vykreslenie
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )
    
    # Pridanie otázky do objektu Conversation
    st.session_state.conversation.add_user(question)
    
    # Okamžité vykreslenie otázky na obrazovku
    with st.chat_message("user"):
        st.markdown(question)
        
    # 2. Generovanie a postupné streamovanie odpovede asistenta
    with st.chat_message("assistant"):
        placeholder = st.empty()
        answer = ""
        citations = ""  # Sem si uložíme citácie, ktoré prídu na konci
        
        with st.spinner("🔍 Searching database & thinking..."):
            chunks = ask(
                question, 
                current_filter, 
                conversation=st.session_state.conversation, 
                debug=False
            )
            try:
                # Načítame prvý kúsok, ktorý prichádza ako dvojica (chunk, chunk_citations)
                first_chunk, first_citations = next(chunks)
                answer += first_chunk
                placeholder.markdown(answer + "▌")
            except StopIteration:
                first_chunk = None

        if first_chunk is not None:
            for chunk, chunk_citations in chunks:
                answer += chunk
                # Ak v tomto kroku prišli citácie, uložíme si ich
                if chunk_citations:
                    citations = chunk_citations
                placeholder.markdown(answer + "▌")
            
            # Zobrazíme finálny text bez blikajúceho kurzora
            placeholder.markdown(answer)

        # 3. Zobrazenie zdrojov cez rozbaľovací expander
        if citations:
            with st.expander("📚 Sources"):
                st.markdown(citations)

        # 4. Uloženie odpovede a citácií
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "citations": citations 
            }
        )
        
        st.session_state.conversation.add_assistant(answer)
        st.rerun()

# ---------------- KROK 5 – Footer ----------------
st.divider()
st.caption("Built with Python, Ollama and ChromaDB")