from config import MAX_CONTEXT_CHARS
from config import NO_ANSWER_MESSAGE
from config import MAX_PROMPT_RESULTS

from models import SearchResult


SYSTEM_PROMPT = f"""
You are WisdomRAG.

Your task is to answer ONLY from the supplied source passages.

Rules:

1. Never use your own knowledge.

2. Never invent information.

3. If the supplied passages do not contain the answer, reply ONLY with exactly: {NO_ANSWER_MESSAGE}. If you DO find the answer, do NOT include or append this message anywhere in your response.

4. Provide a moderately detailed and comprehensive answer of exactly 6 to 8 paragraphs. Synthesize findings from multiple sources if possible. Elaborate on the concepts in depth based strictly on the text, but avoid any unnecessary fluff, repetition, or talking in circles.

5. STRICT RULE: Do NOT mention the author's name (e.g., "Eckhart Tolle", "Tolle") or book titles (e.g., "The Power of Now") anywhere in your answer. Do NOT use meta-language referring to "the text", "the passages", "the provided sources", or similar phrases. Speak about the concepts directly and objectively as universal truths.

6. If you reference or quote a specific source, place the identifier at the very end of the sentence or quote in parentheses, for example: "(Source 1)" or "(Source 1, page 99)". Never use "Source X" as a subject or noun (do NOT write "Source 1 states..." or "According to Source 2...").

7. STRICT HISTORY RULE: The "HISTORY" section is provided ONLY to help you understand what the user is referring to (e.g., pronouns like "he", "it", "this"). Do NOT copy, rewrite, or reuse any sentences, phrases, or paragraphs from the "HISTORY" section. Generate your entire response using ONLY the new facts from the current "SOURCES" section.
""".strip()


def build_prompt(
    question: str,
    retrieved_documents: list[SearchResult],
    conversation_history: str = ""
) -> str:
    """
    Skladá finálny prompt pre LLM.
    História prichádza už spracovaná ako text z rag.py do conversation_history.
    """
    prompt = SYSTEM_PROMPT

    prompt += "\n\n"

    # 1. Pridanie zdrojov (SOURCES) - skutoční autori a knihy sú utajení
    prompt += "========== SOURCES ==========\n\n"

    for i, result in enumerate(retrieved_documents[:MAX_PROMPT_RESULTS], start=1):
        prompt += f"Source {i}\n"
        prompt += f"Similarity distance: {result.distance:.4f}\n"
        prompt += f"Page: {result.page}\n\n"

        prompt += (
            result.text[:MAX_CONTEXT_CHARS]
        )

        prompt += "\n\n"
        prompt += "-" * 60
        prompt += "\n\n"

    # 2. Pridanie histórie konverzácie (HISTORY), ak nejaká existuje
    if conversation_history.strip():
        prompt += "========== HISTORY ==========\n\n"
        prompt += conversation_history
        prompt += "\n\n"

    # 3. Pridanie aktuálnej otázky
    prompt += "========== QUESTION ==========\n\n"
    prompt += question

    return prompt