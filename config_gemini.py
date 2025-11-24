import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()

# Lê a chave do ambiente
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("⚠️ Atenção: variável GEMINI_API_KEY não encontrada. Defina-a no arquivo .env antes de iniciar o app.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
