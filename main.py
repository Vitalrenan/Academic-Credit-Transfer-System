import streamlit as st
import pandas as pd
import base64
import time
import os
from google import genai
from ai_engine import analyze_equivalence_high_accuracy
import PyPDF2

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Sistema de Equivalência - Cruzeiro do Sul",
    page_icon="🎓",
    layout="wide"
)

# --- 2. GESTÃO DE ESTADO (SESSION STATE) ---
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "analise_confirmada" not in st.session_state:
    st.session_state.analise_confirmada = False
if "dados_finais" not in st.session_state:
    st.session_state.dados_finais = None
if "raw_result" not in st.session_state:
    st.session_state.raw_result = None
if "usage_data" not in st.session_state:
    st.session_state.usage_data = None
if "student_name" not in st.session_state:
    st.session_state.student_name = ""

# --- 3. MODAL DE LOGIN ---
@st.dialog("Acesso ao Sistema DataEDUCA")
def login_modal():
    st.write("Identifique-se para aceder ao sistema de validação.")
    nome = st.text_input("Nome do Validador")
    email = st.text_input("E-mail Corporativo")
    
    if st.button("Entrar", type="primary"):
        if nome and "@" in email:
            st.session_state.user_info = {"nome": nome, "email": email}
            st.rerun()
        else:
            st.error("Por favor, insira dados válidos.")

if not st.session_state.user_info:
    login_modal()
    st.stop()

# --- 4. BRANDING ---
image_path = "logo.png" 
if os.path.exists(image_path):
    st.image(image_path, width=600)
else:
    st.markdown(
        """
        <div style="background-color: #003580; color: white; padding: 15px 5px; border-radius: 8px; text-align: center; width: 200px;">
            <div style="font-size: 24px;">⭐</div>
            <div style="font-weight: bold; font-size: 14px;">CRUZEIRO<br>DO SUL</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("Transferência de Créditos - Análise de Equivalência")
st.markdown(f"**Validador:** {st.session_state.user_info['nome']} | **Tecnologia:** Gemini 2.5 Pro")

st.divider()

# --- 5. FUNÇÕES UTILITÁRIAS ---

def calcular_custo(usage):
    if not usage: return 0.0, 0
    try:
        input_tokens = getattr(usage, 'prompt_token_count', 0)
        output_tokens = getattr(usage, 'candidates_token_count', 0)
        total_tokens = getattr(usage, 'total_token_count', 0)
        custo_usd = (input_tokens / 1_000_000 * 1.25) + (output_tokens / 1_000_000 * 3.75)
        return custo_usd * 6.00, total_tokens
    except:
        return 0.0, 0

def extract_text(uploaded_file):
    if not uploaded_file: return ""
    uploaded_file.seek(0)
    try:
        if uploaded_file.name.endswith('.pdf'):
            reader = PyPDF2.PdfReader(uploaded_file)
            return "".join([page.extract_text() or "" for page in reader.pages])
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            return df.to_string()
        elif uploaded_file.name.endswith('.txt'):
            return uploaded_file.read().decode("utf-8")
    except Exception as e:
        return f"Erro de Leitura: {str(e)}"
    return ""

# --- 6. BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configurações")
    api_key = st.text_input("Gemini API Key", type="password")
    file_student = st.file_uploader("Histórico do Aluno (PDF/TXT)", type=['pdf', 'txt'])
    file_matrix = st.file_uploader("Matriz de Referência (XLSX)", type=['xlsx'])
    btn_run = st.button("🚀 Iniciar Análise IA", type="primary", use_container_width=True)

# --- 7. LÓGICA DE PROCESSAMENTO ---
if btn_run:
    if not api_key or not file_student or not file_matrix:
        st.warning("Preencha a API Key e carregue os documentos.")
    else:
        with st.spinner("🤖 Analisando matriz completa e histórico..."):
            txt_student = extract_text(file_student)
            txt_matrix = extract_text(file_matrix)
            data, usage = analyze_equivalence_high_accuracy(api_key, txt_student, txt_matrix)
            if data:
                df = pd.DataFrame(data.get("analise", []))
                if not df.empty:
                    df["Aprovar"] = df["Veredito"].apply(lambda x: True if x == "DEFERIDO" else False)
                st.session_state.raw_result = df
                st.session_state.student_name = data.get("nome_aluno", "Não Identificado")
                st.session_state.usage_data = usage
                st.session_state.analise_confirmada = False
                st.rerun()

# --- 8. INTERFACE DE ABAS ---
if file_student or file_matrix:
    abas = ["📄 Documentos", "🤖 Validação IA"]
    if st.session_state.analise_confirmada:
        abas.append("✅ Relatório Final")
    tabs = st.tabs(abas)

    # --- ABA 1: DOCUMENTOS (ESTRUTURA SOLICITADA) ---
    with tabs[0]:
        col_esq, col_dir = st.columns(2)
        
        with col_esq:
            st.subheader("Histórico do Aluno")
            # Tenta mostrar o histórico como DataFrame se já tiver sido processado pela IA
            if st.session_state.raw_result is not None:
                st.markdown("**Versão Processada (DataFrame):**")
                historico_df = st.session_state.raw_result[["Disciplina_Origem"]].drop_duplicates()
                st.dataframe(historico_df, use_container_width=True, hide_index=True)
            
            st.markdown("**Texto na Íntegra:**")
            texto_completo = extract_text(file_student)
            st.text_area("Conteúdo Original", texto_completo, height=400, disabled=True)
            
        with col_dir:
            st.subheader("Matriz Curricular do Curso")
            if file_matrix:
                file_matrix.seek(0)
                df_matriz_view = pd.read_excel(file_matrix, engine='openpyxl')
                st.dataframe(df_matriz_view, use_container_width=True, height=600)

    # --- ABA 2: VALIDAÇÃO ---
    with tabs[1]:
        if st.session_state.raw_result is not None:
            st.subheader(f"Análise: {st.session_state.student_name}")
            edited_df = st.data_editor(
                st.session_state.raw_result,
                column_config={
                    "Aprovar": st.column_config.CheckboxColumn("Validar?"),
                    "Similaridade": st.column_config.ProgressColumn("Confiança", min_value=0, max_value=1),
                    "Justificativa": st.column_config.TextColumn("Racional IA", width="large")
                },
                use_container_width=True, hide_index=True
            )
            custo_brl, tokens = calcular_custo(st.session_state.usage_data)
            st.info(f"📊 Tokens: {tokens} | Custo: R$ {custo_brl:.4f}")
            if st.button("🔒 Confirmar Validação"):
                st.session_state.dados_finais = edited_df
                st.session_state.analise_confirmada = True
                st.rerun()

    # --- ABA 3: RELATÓRIO FINAL ---
    if st.session_state.analise_confirmada:
        with tabs[2]:
            df_v = st.session_state.dados_finais
            aprovadas = df_v[df_v["Aprovar"] == True]
            nomes_aprovados = aprovadas["Disciplina_Destino"].tolist()
            
            file_matrix.seek(0)
            df_m = pd.read_excel(file_matrix, engine='openpyxl')
            col_n = next((c for c in df_m.columns if any(x in c.lower() for x in ["disciplina", "nome", "matéria"])), df_m.columns[1])
            df_p = df_m[~df_m[col_n].isin(nomes_aprovados)]
            
            st.header(f"Parecer Final: {st.session_state.student_name}")
            k1, k2, k3 = st.columns(3)
            k1.metric("Aproveitadas", len(aprovadas))
            k2.metric("Pendentes", len(df_p))
            k3.metric("Tokens", tokens)

            cl, cr = st.columns(2)
            with cl:
                st.success("### ✅ Aprovadas")
                st.table(aprovadas[["Disciplina_Origem", "Disciplina_Destino"]])
            with cr:
                st.warning("### 📚 Grade Restante (Pendente)")
                st.table(df_p[[col_n]])

            report = f"ALUNO: {st.session_state.student_name}\n\nPENDENTES:\n{df_p[col_n].to_string(index=False)}"
            st.download_button("📥 Baixar Relatório", report, file_name="plano_estudos.txt")