#config.py
import os

#VERSION = "1.0.0"
# AI model
LLM_MODEL = "llama3.2:3b"


# Embedding model
EMBEDDING_MODEL = "nomic-embed-text"


# Koľko výsledkov z databázy chceme
TOP_K = 8

# to je skoro akoby som dal TOP_K = 4, ale takto pri TOP_K = 8 mam niekde k dispozicii aj posledne 4
MAX_PROMPT_RESULTS = 4 

# približný počet slov v jednom chunke
#CHUNK_SIZE_WORDS = 250
CHUNK_SIZE_WORDS = 400 # cela strana ma napr. 470 slov
#CHUNK_SIZE_WORDS = 100
#CHUNK_SIZE_WORDS = 350

# koľko slov sa zopakuje
#CHUNK_OVERLAP_WORDS = 50
CHUNK_OVERLAP_WORDS = 100
#CHUNK_OVERLAP_WORDS = 30
#CHUNK_OVERLAP_WORDS = 80

from pathlib import Path

# Tento riadok zistí absolútnu cestu ku koreňu tvojho projektu
BASE_DIR = Path(__file__).resolve().parent.parent

# Nastavenie presnej absolútnej cesty k databáze
CHROMA_PATH = str(BASE_DIR / "chroma_db")
# Umiestnenie databázy
#CHROMA_PATH = "../chroma_db"


# Knihy
BOOKS_PATH = "../corpora"

# Maximálny počet znakov z jedného chunku,
# ktoré vložíme do promptu.
#MAX_CONTEXT_CHARS = 1500
MAX_CONTEXT_CHARS = 2500
#MAX_CONTEXT_CHARS = 1000
#MAX_CONTEXT_CHARS = 3500

# Ak AI nevie odpoveď nájsť,
# musí odpovedať presne touto vetou.
NO_ANSWER_MESSAGE = (
    "I could not find an answer to this question "
    "in the available input texts."
)

# Ak je najlepší výsledok horší než tento limit,
# AI vôbec nebude volať LLM.
#MAX_DISTANCE = 0.45
MAX_DISTANCE = 0.75

VERSION = "1.0.0"

# Vypisovať diagnostické informácie?
DEBUG = False