import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega variáveis do .env
load_dotenv()

# Configura a API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("⚠️ Erro: variável GEMINI_API_KEY não encontrada no .env")
    exit()

genai.configure(api_key=GEMINI_API_KEY)

print("✅ Conexão com o Gemini configurada com sucesso!")

# Lista os modelos disponíveis para confirmar o nome correto
models = genai.list_models()

print("\n📋 Modelos disponíveis:")
for m in models:
    print("-", m.name)

# Teste de geração
try:
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    response = model.generate_content(
        "Escreva uma mensagem curta e positiva sobre equilíbrio emocional.")
    print("\n✨ Resposta do Gemini:")
    print(response.text)
except Exception as e:
    print("\n❌ Erro ao gerar conteúdo:", e)
