from google import genai
from google.genai import types
import json
import re

def clean_json_string(text):
    """Limpeza cirúrgica para garantir JSON válido."""
    # Remove blocos markdown (```json ... ```)
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    
    # Isola o objeto JSON (encontra o primeiro { e o último })
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1:
        return text[start : end + 1]
    
    return text.strip()

def analyze_equivalence_high_accuracy(api_key, text_student, text_syllabus):
    if not api_key:
        return {"nome_aluno": "Erro: API Key não fornecida", "analise": []}, None

    try:
        # --- NOVA SINTAXE (Client v1.0 / 2026) ---
        client = genai.Client(api_key=api_key)
        
        # Vamos usar o Gemini 2.5 Pro (Equilíbrio perfeito de raciocínio e custo)
        # Se quiser mais velocidade, troque por 'gemini-2.5-flash'
        MODEL_ID = 'gemini-2.5-pro' 
        
        prompt = f"""
        Você é um Coordenador Acadêmico Especialista.
        
        TAREFA: Comparar Histórico Escolar (Origem) com Matriz Curricular (Destino).
        
        DOCUMENTO 1 (Histórico do Aluno):
        {text_student[:50000]}

        DOCUMENTO 2 (Matriz da Instituição):
        {text_syllabus[:50000]}

        OBJETIVO:
        1. Identificar o Nome do Aluno.
        2. Listar disciplinas APROVADAS no histórico e encontrar equivalentes na matriz.
        3. Para cada par, decidir: DEFERIDO (Equivalente) ou INDEFERIDO.
        
        FORMATO JSON OBRIGATÓRIO:
        {{
            "nome_aluno": "Nome Completo",
            "analise": [
                {{
                    "Disciplina_Origem": "Nome no histórico",
                    "Disciplina_Destino": "Nome na matriz",
                    "Carga_Horaria_Comparada": "Ex: 60h vs 80h",
                    "Similaridade": 0.95,
                    "Veredito": "DEFERIDO",
                    "Justificativa": "Explicação técnica"
                }}
            ]
        }}
        """

        # Configuração da Geração
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1, # Baixa temperatura para precisão
                response_mime_type='application/json' # Força JSON estruturado
            )
        )
        
        # Processamento da resposta
        cleaned_text = clean_json_string(response.text)
        
        try:
            data = json.loads(cleaned_text)
        except:
            # Fallback: remove quebras de linha se o JSON estiver quebrado
            cleaned_text = cleaned_text.replace('\n', ' ')
            data = json.loads(cleaned_text)

        # Garante estrutura mínima para não quebrar a tela
        if "analise" not in data: data["analise"] = []
        if "nome_aluno" not in data: data["nome_aluno"] = "Aluno Não Identificado"
            
        return data, response.usage_metadata

    except Exception as e:
        error_msg = str(e)
        print(f"Erro Engine: {error_msg}")
        
        user_msg = f"Erro Técnico: {error_msg[:100]}"
        if "404" in error_msg:
            user_msg = f"Erro 404: O modelo {MODEL_ID} não está habilitado na sua chave."
        elif "429" in error_msg:
            user_msg = "Erro 429: Cota excedida. Aguarde um momento."
            
        return {"nome_aluno": user_msg, "analise": []}, None