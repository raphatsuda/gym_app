import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração Mobile
st.set_page_config(page_title="Treino Raphael", layout="centered")

# Dicionário mestre com Metas (Séries e Reps)
dados_treino = {
    "TREINO A (Superior)": {
        "Supino Máquina Sentado": {"sub": "Supino Halteres (Neutro)", "sets": 3, "reps": 15},
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

# Inicializar contador de séries na memória do app
if 'progresso' not in st.session_state:
    st.session_state.progresso = {}

st.title("💪 Raphael: Tônus & Saúde")

# 1. Seleção de Treino
treino_sel = st.selectbox("Treino de hoje:", list(dados_treino.keys()))
exercicios = dados_treino[treino_sel]

# 2. Seleção de Exercício
ex_base = st.selectbox("Exercício:", list(exercicios.keys()))
info = exercicios[ex_base]
meta_sets = info['sets']
meta_reps = info['reps']

# 3. Gerenciador de Substitutos
usar_sub = st.checkbox(f"Usar substituto: {info['sub']}")
nome_final = info['sub'] if usar_sub else ex_base

# Chave única para o contador deste exercício
chave_ex = f"{treino_sel}_{nome_final}"
if chave_ex not in st.session_state.progresso:
    st.session_state.progresso[chave_ex] = 0

# 4. Painel de Controle de Séries
st.info(f"🎯 **Meta:** {meta_sets} séries de {meta_reps} reps")
sets_feitos = st.session_state.progresso[chave_ex]

# Barra de progresso visual
progresso_visual = min(sets_feitos / meta_sets, 1.0)
st.progress(progresso_visual)
st.write(f"✅ Série **{sets_feitos}** de **{meta_sets}** concluída(s)")

st.divider()

# 5. Registro da Série Atual
col1, col2 = st.columns(2)
with col1:
    peso = st.number_input("Carga (kg)", min_value=0.0, step=0.5, format="%.1f")
with col2:
    reps_feitas = st.number_input("Reps feitas", min_value=0, value=meta_reps)

nota = st.text_input("Nota (ex: dor, esforço 1-10)", "")

if st.button("💾 REGISTRAR SÉRIE"):
    # Incrementar contador local
    st.session_state.progresso[chave_ex] += 1
    
    # Salvar no CSV
    novo_log = pd.DataFrame([{
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Exercicio": nome_final,
        "Peso": peso,
        "Reps": reps_feitas,
        "Serie_Num": st.session_state.progresso[chave_ex],
        "Nota": nota
    }])
    
    file_name = "historico_treino.csv"
    if not os.path.isfile(file_name):
        novo_log.to_csv(file_name, index=False)
    else:
        novo_log.to_csv(file_name, mode='a', header=False, index=False)
    
    st.rerun() # Atualiza a tela para mostrar o novo número de séries

# 6. Finalização e Histórico
st.divider()
col_left, col_right = st.columns(2)

with col_left:
    if st.button("🏁 Finalizar Treino (Limpar Contadores)"):
        st.session_state.progresso = {}
        st.success("Contadores zerados para o próximo treino!")
        st.rerun()

with col_right:
    if st.checkbox("📊 Ver Histórico"):
        if os.path.isfile("historico_treino.csv"):
            df = pd.read_csv("historico_treino.csv")
            st.dataframe(df.tail(15), use_container_width=True)

st.caption("🚴 Lembrete: 30 min de Cardio após a musculação!")
