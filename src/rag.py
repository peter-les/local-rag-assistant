# rag.py
from retriever import retrieve
from prompt_builder import build_prompt
from chat_model import ask_llm_stream
from confidence import has_enough_confidence
from config import NO_ANSWER_MESSAGE
from citations import build_citations
from config import DEBUG
from config import MAX_PROMPT_RESULTS

def ask(question, search_filter=None, conversation=None, debug=True):
    # 1. Informujeme, že prehľadávame databázu
    print("🔍 Searching database for relevant passages...", end="", flush=True)
    
    search_question = question

    if conversation is not None:

        history = conversation.last_user_questions()

        if history:
            search_question = history + "\n" + question

    results = retrieve(
        search_question,
        search_filter
    )

    # Zmažeme správu o vyhľadávaní z konzoly, aby neprekážala debug výpisom
    print("\r" + " " * 60 + "\r", end="", flush=True)

    # === TU SÚ DEBUG VÝPISY ===
    if debug:
        if DEBUG:
            print(f"\n[DEBUG] Found {len(results)} chunks.")
            for i, r in enumerate(results):
                print(f"  -> Chunk {i+1}: {r.book}, Strana: {r.page} (Distance: {r.distance:.4f})")
    # ==========================

    if not has_enough_confidence(results):
        # Ak nemáme dostatočnú istotu, vrátime zoznam s chybovou hláškou a prázdnymi citáciami
        yield NO_ANSWER_MESSAGE, ""
        return

    # === KROK 1: Vytiahnutie histórie z pamäťového objektu ===
    history = ""
    if conversation is not None:
        # Voláme metódu last_messages() z tvojej novej triedy Conversation
        history = conversation.last_messages()

    # Skladáme prompt. Parametre pomenujeme presne podľa nového prompt_builder.py
    prompt = build_prompt(
        question=question,
        retrieved_documents=results,
        conversation_history=history
    )

    # 2. Informujeme, že model teraz číta texty a pripravuje odpoveď
    print("🧠 Thinking and formulating answer (this may take a moment)...", end="", flush=True)

    # Zostavíme si vopred citácie, ktoré neskôr vrátime oddelene
    citations = build_citations(results[:MAX_PROMPT_RESULTS])

    # Postupne posielame kúsky odpovede z LLM
    first_chunk = True
    for chunk in ask_llm_stream(prompt):
        # Akonáhle dorazí úplne prvý kúsok odpovede, zmažeme stavovú správu v konzole
        if first_chunk:
            print("\r" + " " * 70 + "\r", end="", flush=True)
            first_chunk = False
            
        # VÝZNAMNÁ ZMENA: Každý krok streamu vracia dvojicu (kúsok_textu, citácie)
        # Počas streamovania odpovede posielame citácie prázdne (""), aby sa nevykresľovali predčasne
        yield chunk["message"]["content"], ""

    # Na úplnom konci po úspešnom dostreamovaní pošleme ako poslednú vec hotové citácie
    yield "", citations