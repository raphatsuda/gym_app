import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração Mobile
st.set_page_config(page_title="Treino Raphael", layout="centered")

# Dicionário de Treinos
dados_treino = {
    "TREINO A (Superior)": {
        "Supino Máquina (Alavanca/Pino)": {"sub": "Crucifixo Máquina (Voador)", "sets": 3, "reps": 15},
        "Crucifixo Máquina (Voador)": {"sub": "Crossover (Polia)", "sets": 3, "reps": 15},
        "Remada Baixa Triângulo": {"sub": "Puxada Pegada Supinada", "sets": 3, "reps": 15},
        "Puxada Alta Aberta": {"sub": "Puxada com Triângulo", "sets": 3, "reps": 15},
        "Elevação Lateral": {"sub": "Elevação Lateral no Cabo", "sets": 3, "reps": 15},
        "Rosca Direta Barra W": {"sub": "Rosca Martelo Halteres", "sets": 3, "reps": 12},
        "Tríceps na Polia (Corda)": {"sub": "Tríceps Barra W no Cabo", "sets": 3, "reps": 15}
    },
    "TREINO B (Inferior/Core)": {
        "Leg Press (45 ou Horiz.)": {"sub": "Agachamento Goblet (Halter)", "sets": 3, "reps": 15},
        "Agachamento no Smith": {"sub": "Cadeira Adutora", "sets": 3, "reps": 12},
        "Cadeira Extensora": {"sub": "Agachamento Livre (Baixa Carga)", "sets": 3, "reps": 15},
        "Cadeira ou Mesa Flexora": {"sub": "Elevação Pélvica", "sets": 3, "reps": 15},
        "Panturrilha em Pé": {"sub": "Panturrilha no Degrau", "sets": 4, "reps": 15},
        "Máquina Abdominal": {"sub": "Abdominal Infra no solo", "sets": 3, "reps": 20},
        "Banco Romano (Lombar)": {"sub": "Prancha Estática", "sets": 3, "reps": 12}
    }
}

FILE_NAME = "historico_treino.csv"

# Inicializar memória
if 'progresso' not in st.session_state:
    st.session_state.progresso = {}

# Função segura para salvar dados (Evita perda no recarregamento)
def salvar_dados(treino, exercicio, peso, reps, serie, nota):
    novo_log = pd.DataFrame([{
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Treino": treino,
        "Exercicio": exercicio,
        "Peso": peso,
        "Reps": reps,
        "Serie_Num": serie,
        "Nota": nota
    }])
    if not os.path.isfile(FILE_NAME):
        novo_log.to_csv(FILE_NAME, index=False)
    else:
        novo_log.to_csv(FILE_NAME, mode='a', header=False, index=False)

st.title("💪 Raphael: Tônus & Saúde")

# 1. Seleção
treino_sel = st.selectbox("Treino de hoje:", list(dados_treino.keys()))
ex_base = st.selectbox("Exercício:", list(dados_treino[treino_sel].keys()))
info = dados_treino[treino_sel][ex_base]

usar_sub = st.checkbox(f"Usar substituto: {info['sub']}")
nome_final = info['sub'] if usar_sub else ex_base

# 2. Busca do Último Registro
last_weight = 0.0
last_reps = info['reps']

if os.path.isfile(FILE_NAME):
    df_hist = pd.read_csv(FILE_NAME)
    historico_ex = df_hist[df_hist['Exercicio'] == nome_final]
    if not historico_ex.empty:
        ultimo_log = historico_ex.iloc[-1]
        last_weight = float(ultimo_log['Peso'])
        last_reps = int(ultimo_log['Reps'])
        st.caption(f"⬅️ **Último Treino:** {last_weight}kg x {last_reps} reps")

st.divider()

# 3. Controle de Séries
chave_ex = f"{treino_sel}_{nome_final}"
if chave_ex not in st.session_state.progresso:
    st.session_state.progresso[chave_ex] = 0

meta_sets = info['sets']
sets_feitos = st.session_state.progresso[chave_ex]
st.write(f"🎯 Meta: {meta_sets} séries | ✅ Feitas: **{sets_feitos}**")
st.progress(min(sets_feitos / meta_sets, 1.0))

# 4. Input Inteligente (Os campos ficam vazios, fáceis de digitar)
col1, col2 = st.columns(2)
with col1:
    peso_input = st.number_input("Peso (kg)", value=None, placeholder=f"{last_weight} (Deixe vazio p/ repetir)", step=0.5, format="%.1f")
with col2:
    reps_input = st.number_input("Reps", value=None, placeholder=f"{last_reps} (Deixe vazio p/ repetir)", step=1)

nota = st.text_input("Nota / Sensibilidade (Opcional)", "")

if st.button("💾 REGISTRAR SÉRIE", use_container_width=True):
    # Se o usuário não digitou nada, assume o valor do último treino
    peso_final = peso_input if peso_input is not None else last_weight
    reps_final = reps_input if reps_input is not None else last_reps
    
    st.session_state.progresso[chave_ex] += 1
    salvar_dados(treino_sel, nome_final, peso_final, reps_final, st.session_state.progresso[chave_ex], nota)
    st.success(f"Série {st.session_state.progresso[chave_ex]} salva com sucesso!")
    st.rerun()

st.divider()

# 5. Módulo de Cardio
st.subheader("🏃 Registro de Cardio")
col_c1, col_c2 = st.columns(2)
with col_c1:
    tempo_cardio = st.number_input("Minutos", value=None, placeholder="30", step=5)
with col_c2:
    tipo_cardio = st.selectbox("Equipamento", ["Elíptico", "Bicicleta", "Esteira", "Não fiz hoje"])

if st.button("Salvar Cardio"):
    tempo_final = tempo_cardio if tempo_cardio is not None else 30
    if tipo_cardio == "Não fiz hoje":
        tempo_final = 0
    salvar_dados(treino_sel, "Cardio", 0, tempo_final, 1, tipo_cardio)
    st.success("Cardio registrado!")

st.divider()

# 6. Histórico Visual Organizado por Dia
st.subheader("📅 Meu Histórico")

if os.path.isfile(FILE_NAME):
    df_full = pd.read_csv(FILE_NAME)
    if not df_full.empty:
        # Extrai apenas a data (sem a hora) para agrupar
        df_full['Apenas_Data'] = df_full['Data'].str.split(' ').str[0]
        
        # Pega os últimos 5 dias de treino
        ultimos_dias = df_full['Apenas_Data'].unique()[-5:][::-1]
        
        for dia in ultimos_dias:
            treinos_do_dia = df_full[df_full['Apenas_Data'] == dia]
            with st.expander(f"Treino do dia: {dia}"):
                for _, row in treinos_do_dia.iterrows():
                    if row['Exercicio'] == "Cardio":
                        st.write(f"🏃 **Cardio:** {row['Reps']} min ({row['Nota']})")
                    else:
                        st.write(f"🏋️ **{row['Exercicio']}** - Série {row['Serie_Num']} | {row['Peso']}kg x {row['Reps']} reps")
    else:
        st.info("Nenhum dado salvo.")
else:
    st.info("O histórico aparecerá aqui após o primeiro treino.")

if st.button("🏁 Resetar Contadores (Fim do Treino)"):
    st.session_state.progresso = {}
    st.rerun()
