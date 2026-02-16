import pandas as pd

# --- 1. CRIANDO A MATRIZ DE REFERÊNCIA COMPLETA (CRUZEIRO DO SUL - 10 SEMESTRES) ---
# Curso Base: Engenharia de Computação
# Estrutura: Ciclo Básico (1-4) + Ciclo Profissionalizante (5-8) + Finalização (9-10)

dados_matriz_completa = [
    # --- 1º SEMESTRE ---
    {"Semestre": 1, "Código": "MAT101", "Disciplina": "Cálculo Diferencial e Integral I", "Carga_Horaria": 80},
    {"Semestre": 1, "Código": "FIS101", "Disciplina": "Física Geral e Experimental I", "Carga_Horaria": 80},
    {"Semestre": 1, "Código": "COMP101", "Disciplina": "Algoritmos e Programação", "Carga_Horaria": 80},
    {"Semestre": 1, "Código": "QUI101", "Disciplina": "Química Tecnológica Geral", "Carga_Horaria": 40},
    {"Semestre": 1, "Código": "HUM101", "Disciplina": "Sociedade e Tecnologia", "Carga_Horaria": 40},
    {"Semestre": 1, "Código": "ENG100", "Disciplina": "Introdução à Engenharia", "Carga_Horaria": 40},

    # --- 2º SEMESTRE ---
    {"Semestre": 2, "Código": "MAT102", "Disciplina": "Cálculo Diferencial e Integral II", "Carga_Horaria": 80},
    {"Semestre": 2, "Código": "FIS102", "Disciplina": "Física Geral e Experimental II", "Carga_Horaria": 80},
    {"Semestre": 2, "Código": "DES101", "Disciplina": "Desenho Técnico Projetivo", "Carga_Horaria": 40},
    {"Semestre": 2, "Código": "MAT103", "Disciplina": "Geometria Analítica e Álgebra Linear", "Carga_Horaria": 80},
    {"Semestre": 2, "Código": "COMP102", "Disciplina": "Lógica de Programação e Algoritmos", "Carga_Horaria": 80},

    # --- 3º SEMESTRE ---
    {"Semestre": 3, "Código": "MAT201", "Disciplina": "Equações Diferenciais Ordinárias", "Carga_Horaria": 80},
    {"Semestre": 3, "Código": "MEC101", "Disciplina": "Mecânica Geral (Estática e Dinâmica)", "Carga_Horaria": 80},
    {"Semestre": 3, "Código": "COMP201", "Disciplina": "Estrutura de Dados", "Carga_Horaria": 80},
    {"Semestre": 3, "Código": "ELE101", "Disciplina": "Eletricidade Aplicada", "Carga_Horaria": 40},
    {"Semestre": 3, "Código": "EST101", "Disciplina": "Probabilidade e Estatística", "Carga_Horaria": 60},

    # --- 4º SEMESTRE ---
    {"Semestre": 4, "Código": "MAT202", "Disciplina": "Cálculo Numérico", "Carga_Horaria": 40},
    {"Semestre": 4, "Código": "ELE201", "Disciplina": "Circuitos Elétricos I", "Carga_Horaria": 80},
    {"Semestre": 4, "Código": "FIS201", "Disciplina": "Fenômenos de Transportes", "Carga_Horaria": 40},
    {"Semestre": 4, "Código": "COMP202", "Disciplina": "Programação Orientada a Objetos", "Carga_Horaria": 80},
    {"Semestre": 4, "Código": "ELE202", "Disciplina": "Eletrônica Digital", "Carga_Horaria": 80},

    # --- 5º SEMESTRE ---
    {"Semestre": 5, "Código": "COMP301", "Disciplina": "Banco de Dados", "Carga_Horaria": 80},
    {"Semestre": 5, "Código": "COMP302", "Disciplina": "Engenharia de Software", "Carga_Horaria": 80},
    {"Semestre": 5, "Código": "ELE301", "Disciplina": "Arquitetura e Organização de Computadores", "Carga_Horaria": 80},
    {"Semestre": 5, "Código": "ELE302", "Disciplina": "Microprocessadores e Microcontroladores", "Carga_Horaria": 80},
    {"Semestre": 5, "Código": "MAT301", "Disciplina": "Matemática Discreta", "Carga_Horaria": 40},

    # --- 6º SEMESTRE ---
    {"Semestre": 6, "Código": "COMP303", "Disciplina": "Sistemas Operacionais", "Carga_Horaria": 80},
    {"Semestre": 6, "Código": "COMP304", "Disciplina": "Redes de Computadores I", "Carga_Horaria": 80},
    {"Semestre": 6, "Código": "COMP305", "Disciplina": "Inteligência Artificial e Machine Learning", "Carga_Horaria": 80},
    {"Semestre": 6, "Código": "COMP306", "Disciplina": "Compiladores e Linguagens Formais", "Carga_Horaria": 60},
    {"Semestre": 6, "Código": "PROJ600", "Disciplina": "Projeto Integrador em Computação I", "Carga_Horaria": 40},

    # --- 7º SEMESTRE ---
    {"Semestre": 7, "Código": "COMP401", "Disciplina": "Redes de Computadores II", "Carga_Horaria": 80},
    {"Semestre": 7, "Código": "COMP402", "Disciplina": "Segurança da Informação", "Carga_Horaria": 40},
    {"Semestre": 7, "Código": "COMP403", "Disciplina": "Sistemas Distribuídos", "Carga_Horaria": 60},
    {"Semestre": 7, "Código": "ELE401", "Disciplina": "Sistemas Embarcados", "Carga_Horaria": 80},
    {"Semestre": 7, "Código": "ADM101", "Disciplina": "Empreendedorismo e Gestão", "Carga_Horaria": 40},

    # --- 8º SEMESTRE ---
    {"Semestre": 8, "Código": "COMP404", "Disciplina": "Computação Gráfica e Processamento de Imagens", "Carga_Horaria": 80},
    {"Semestre": 8, "Código": "COMP405", "Disciplina": "Internet das Coisas (IoT)", "Carga_Horaria": 60},
    {"Semestre": 8, "Código": "COMP406", "Disciplina": "Teste e Qualidade de Software", "Carga_Horaria": 40},
    {"Semestre": 8, "Código": "ADM102", "Disciplina": "Gestão de Projetos", "Carga_Horaria": 40},
    {"Semestre": 8, "Código": "OPT001", "Disciplina": "Optativa I", "Carga_Horaria": 40},

    # --- 9º SEMESTRE ---
    {"Semestre": 9, "Código": "TCC100", "Disciplina": "Trabalho de Conclusão de Curso I", "Carga_Horaria": 40},
    {"Semestre": 9, "Código": "ESTG100", "Disciplina": "Estágio Supervisionado I", "Carga_Horaria": 160},
    {"Semestre": 9, "Código": "HUM200", "Disciplina": "Ética e Legislação Profissional", "Carga_Horaria": 40},
    {"Semestre": 9, "Código": "OPT002", "Disciplina": "Optativa II", "Carga_Horaria": 40},
    {"Semestre": 9, "Código": "COMP501", "Disciplina": "Ciência de Dados e Big Data", "Carga_Horaria": 80},

    # --- 10º SEMESTRE ---
    {"Semestre": 10, "Código": "TCC200", "Disciplina": "Trabalho de Conclusão de Curso II", "Carga_Horaria": 40},
    {"Semestre": 10, "Código": "ESTG200", "Disciplina": "Estágio Supervisionado II", "Carga_Horaria": 160},
    {"Semestre": 10, "Código": "AMB100", "Disciplina": "Ciências do Ambiente e Sustentabilidade", "Carga_Horaria": 40},
    {"Semestre": 10, "Código": "LIBRAS", "Disciplina": "Língua Brasileira de Sinais", "Carga_Horaria": 40},
    {"Semestre": 10, "Código": "OPT003", "Disciplina": "Optativa III", "Carga_Horaria": 40},
]

df_matriz = pd.DataFrame(dados_matriz_completa)
df_matriz.to_excel("mock_matriz_referencia_cruzeiro.xlsx", index=False)
print(f"✅ Arquivo 'mock_matriz_referencia_cruzeiro.xlsx' gerado com {len(df_matriz)} disciplinas!")


# --- 2. CRIANDO O HISTÓRICO ESCOLAR (ALUNO EXTERNO - 4 SEMESTRES) ---
texto_historico = """
UNIVERSIDADE FEDERAL DO EXEMPLO (UFE)
SISTEMA ACADÊMICO - EMISSÃO: 15/02/2026

DADOS DO ALUNO:
Nome: João da Silva Santos
Curso: Engenharia Mecatrônica
Matrícula: 2024.1.0054

HISTÓRICO DE DISCIPLINAS CURSADAS:

--- 1º SEMESTRE (2024.1) ---
DISCIPLINA: Cálculo I
NOTA: 7.5 | STATUS: APROVADO | CH: 60h
(Ementa: Limites, derivadas e introdução à integral)

DISCIPLINA: Física Teórica A
NOTA: 6.0 | STATUS: APROVADO | CH: 60h
(Ementa: Mecânica clássica e leis de Newton)

DISCIPLINA: Laboratório de Física A
NOTA: 8.0 | STATUS: APROVADO | CH: 30h

DISCIPLINA: Introdução à Computação (Python)
NOTA: 9.2 | STATUS: APROVADO | CH: 60h

DISCIPLINA: Química para Engenharia
NOTA: 5.5 | STATUS: APROVADO | CH: 60h

--- 2º SEMESTRE (2024.2) ---
DISCIPLINA: Cálculo II
NOTA: 8.0 | STATUS: APROVADO | CH: 60h

DISCIPLINA: Física Teórica B (Eletromagnetismo)
NOTA: 4.5 | STATUS: REPROVADO | CH: 60h
(Nota: O aluno reprovou nesta matéria, a IA NÃO deve dar equivalência)

DISCIPLINA: Geometria Analítica
NOTA: 7.0 | STATUS: APROVADO | CH: 60h

DISCIPLINA: Expressão Gráfica e Modelagem 3D
NOTA: 10.0 | STATUS: APROVADO | CH: 60h

--- 3º SEMESTRE (2025.1) ---
DISCIPLINA: Equações Diferenciais
NOTA: 7.2 | STATUS: APROVADO | CH: 60h

DISCIPLINA: Mecânica dos Sólidos
NOTA: 8.5 | STATUS: APROVADO | CH: 80h

DISCIPLINA: Algoritmos e Estruturas de Dados
NOTA: 9.0 | STATUS: APROVADO | CH: 60h

--- 4º SEMESTRE (2025.2) ---
DISCIPLINA: Estatística Aplicada
NOTA: 8.0 | STATUS: APROVADO | CH: 60h

DISCIPLINA: Eletrotécnica Básica
NOTA: 7.5 | STATUS: APROVADO | CH: 60h
"""

with open("mock_historico_aluno_externo.txt", "w", encoding="utf-8") as f:
    f.write(texto_historico)

print("✅ Arquivo 'mock_historico_aluno_externo.txt' gerado com sucesso!")