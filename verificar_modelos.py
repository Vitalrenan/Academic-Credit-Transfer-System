# verificar_modelos.py
import google.generativeai as genai
import os

# Cole sua API Key aqui para testar (ou pegue de variável de ambiente)
API_KEY = "AIzaSyC_GbnCQPAuBlVWIxv98npFQRCXIJ04lEs" 

if API_KEY == "AIzaSyC_GbnCQPAuBlVWIxv98npFQRCXIJ04lE":
    print("❌ Erro: Edite o arquivo e coloque sua API Key na linha 5.")
else:
    genai.configure(api_key=API_KEY)
    print("🔍 Consultando modelos disponíveis para sua chave em Fev/2026...\n")
    
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Disponível: {m.name}")
    except Exception as e:
        print(f"❌ Erro ao listar: {e}")