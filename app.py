import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração Mobile
st.set_page_config(page_title="Treino Raphael", layout="centered")

# Dicionário mestre atualizado com CRUCIFIXO MÁQUINA
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

if 'progresso' not in st.session_state:
    st.session_state.progresso = {}

st.title("💪 Raphael: Tônus & Saúde")

# 1. Seleção de Treino e Exercício
treino_sel = st.selectbox("Treino de hoje:", list(dados_treino.keys()))
ex_base = st.selectbox("Exercício:", list(dados_treino[treino_sel].keys()))
info = dados_treino[treino_sel][ex_base]

usar_sub = st.checkbox(f"Usar substituto: {info['sub']}")
nome_final = info['sub'] if usar_sub else ex_base

# 2. Busca do Último Registro
file_name = "historico_treino.csv"
last_weight = 0.0
last_reps = info['reps']

if os.path.isfile(file_name):
    df_hist = pd.read_csv(file_name)
    historico_ex = df_hist[df_hist['Exercicio'] == nome_final]
    if not historico_ex.empty:
        ultimo_log = historico_ex.iloc[-1]
        last_weight = float(ultimo_log['Peso'])
        last_reps = int(ultimo_log['Reps'])
        st.warning(f"⬅️ **Último Treino:** {last_weight}kg x {last_reps} reps")
    else:
        st.info("🆕 Primeiro treino deste exercício!")

st.divider()

# 3. Controle de Séries
chave_ex = f"{treino_sel}_{nome_final}"
if chave_ex not in st.session_state.progresso:
    st.session_state.progresso[chave_ex] = 0

meta_sets = info['sets']
sets_feitos = st.session_state.progresso[chave_ex]
st.write(f"🎯 Meta: {meta_sets} séries | Concluídas: **{sets_feitos}**")
st.progress(min(sets_feitos / meta_sets, 1.0))

# 4. Registro da Série
col1, col2 = st.columns(2)
with col1:
    peso = st.number_input("Peso (kg)", min_value=0.0, value=last_weight, step=0.5, format="%.1f")
with col2:
    reps_feitas = st.number_input("Reps feitas", min_value=0, value=last_reps)

nota = st.text_input("Nota / Percepção de esforço", "")

if st.button("💾 REGISTRAR SÉRIE"):
    st.session_state.progresso[chave_ex] += 1
    novo_log = pd.DataFrame([{
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Exercicio": nome_final,
        "Peso": peso,
        "Reps": reps_feitas,
        "Serie_Num": st.session_state.progresso[chave_ex],
        "Nota": nota
    }])
    
    if not os.path.isfile(file_name):
        novo_log.to_csv(file_name, index=False)
    else:
        novo_log.to_csv(file_name, mode='a', header=False, index=False)
    st.rerun()

# 5. Finalização
st.divider()
if st.button("🏁 Finalizar Treino (Zerar Contadores)"):
    st.session_state.progresso = {}
    st.rerun()

if st.checkbox("📊 Ver Tabela Completa"):
    if os.path.isfile(file_name):
        st.dataframe(pd.read_csv(file_name).tail(20), use_container_width=True)

st.caption("🚴 Cardio: 30 min Elíptico/Bike.")
