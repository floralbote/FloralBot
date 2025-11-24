# app/chatbot.py

import os
from typing import Optional
import google.generativeai as genai

# Carregar chave da API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.0-flash"

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
else:
    model = None


def _build_prompt(user_message: str, context: str, num_user_messages: int) -> str:
    """
    Constrói o prompt com regras claras de fluxo em 3 fases:
    1 → Pergunta 1
    2 → Pergunta 2
    3 → Pergunta 3
    >=4 → Recomendar florais e perguntar se quer mais algo
    """

    return f"""
Você é o FloralBot, um assistente acolhedor especializado nos Florais de Bach.

OBJETIVO:
Conduzir a conversa em CICLOS de 3 perguntas:
- Faça 1 pergunta a cada resposta do usuário.
- Depois da 3ª resposta, PARE de perguntar e:
    1. Sugira 1 a 3 florais adequados.
    2. Explique brevemente cada floral.
    3. Depois pergunte: "Posso te ajudar com mais alguma coisa?"

REGRAS ESSENCIAIS:
1. Nunca recomende florais antes do usuário responder 3 perguntas.
2. Nunca encerre a conversa antes do usuário responder se quer ajuda extra.
3. Se o usuário responder "não", "não precisa", "obrigado", "tchau" etc → encerre com carinho.
4. Se disser que quer mais ajuda → reinicie o ciclo (volta para a pergunta 1).
5. Não repita perguntas.
6. Seja acolhedor, breve, empático e natural.
7. Use o CONTEXTO abaixo somente para entender a conversa e evitar repetir.

=== CONTEXTO DA CONVERSA ===
{context}

=== QUANTAS RESPOSTAS O USUÁRIO JÁ DEU NESTE CICLO ===
{num_user_messages}

=== MENSAGEM ATUAL DO USUÁRIO ===
{user_message}

Agora responda seguindo exatamente as regras acima.
"""


def generate_response(user_message: str, context: str, num_user_messages: int) -> str:
    """Gera resposta usando Gemini ou fallback local."""

    if model is None:
        return f"(Simulação) Você disse: {user_message}"

    prompt = _build_prompt(user_message, context, num_user_messages)

    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text.strip()

        return "Desculpe, não consegui interpretar sua mensagem."

    except Exception as e:
        print("Erro ao chamar Gemini:", e)
        return "Desculpe, estou com dificuldades técnicas no momento. Pode tentar novamente?"
