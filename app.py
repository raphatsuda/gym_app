import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração para visualização mobile
st.set_page_config(page_title="Raphael Gym Log", layout="centered")

# Título e Estilo
st.title("💪 Raphael: Tônus & Saúde")
st.markdown("---")

# Banco de Dados de Exercícios e Substitutos
planilha_treino = {
    "TREINO A (Superior)": {
        "Supino Máquina": "Supino Halteres (Pegada Neutra)",
        "Remada Baixa Triângulo": "Puxada Pegada Supinada",
        "Puxada Alta Aberta": "Puxada com Triângulo",
        "Elevação Lateral": "Elevação Lateral no Cabo",
        "Rosca Direta Barra W": "Rosca Martelo Halteres",
        "Tríceps Corda": "Tríceps Barra W no Cabo"
    },
    "TREINO B (Inferior/Core)": {
        "Leg Press (45 ou Horiz.)": "Agachamento Goblet (Halter)",
        "Agachamento no Smith": "Cadeira Adutora",
        "Cadeira Extensora": "Agachamento Livre (Carga Baixa)",
        "Cadeira ou Mesa Flexora": "Elevação Pélvica",
        "Panturrilha em Pé": "Panturrilha no Degrau",
        "Máquina Abdominal": "Abdominal Infra Solo",
        "Banco Romano (Lombar)": "Prancha Estática"
    }
}

# 1. Seleção do Treino do Dia
treino_dia = st.radio("Qual o treino de hoje?", list(planilha_treino.keys()), horizontal=True)

# 2. Seleção do Exercício
exercicio_principal = st.selectbox("Selecione o Exercício:", list(planilha_treino[treino_dia].keys()))
substituto = planilha_treino[treino_dia][exercicio_principal]

# Toggle para registrar se usou o substituto
usou_substituto = st.checkbox(f"Usei o substituto: {substituto}")

nome_final = substituto if usou_substituto else exercicio_principal

# 3. Registro de Carga e Repetições
st.subheader(f"Registrar: {nome_final}")
col1, col2 = st.columns(2)
with col1:
    peso = st.number_input("Carga (kg)", min_value=0.0, step=0.5, format="%.1f")
with col2:
    reps = st.number_input("Repetições", min_value=0, step=1)

# 4. Monitoramento Articular (Importante para seu histórico)
sensibilidade = st.select_slider(
    "Como estão as articulações (Pulsos/Lombar/Joelhos)?",
    options=["Sem Dor", "Leve Desconforto", "Moderada", "Alerta", "Dor Forte"]
)

nota = st.text_input("Nota adicional (Opcional):", placeholder="Ex: Sentia a lombar no final")

# 5. Lógica de Salvamento
if st.button("💾 SALVAR SÉRIE"):
    novo_log = pd.DataFrame([{
        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Treino": treino_dia,
        "Exercicio": nome_final,
        "Peso": peso,
        "Reps": reps,
        "Articulacao": sensibilidade,
        "Obs": nota
    }])

    # Salva em CSV local (ou cria um se não existir)
    file_name = "historico_treino_raphael.csv"
    if not os.path.isfile(file_name):
        novo_log.to_csv(file_name, index=False)
    else:
        novo_log.to_csv(file_name, mode='a', header=False, index=False)

    st.success(f"Série de {nome_final} salva!")

# 6. Visualização do Histórico
st.markdown("---")
if st.checkbox("📊 Ver meu Histórico Recente"):
    if os.path.isfile("historico_treino_raphael.csv"):
        df_hist = pd.read_csv("historico_treino_raphael.csv")
        st.dataframe(df_hist.tail(10), use_container_width=True)  # Mostra as últimas 10 entradas
    else:
        st.info("Ainda não há registros salvos.")

# 7. Lembrete do Cardio
st.info("🚴 **Lembrete:** Não esqueça dos 30 min de Elíptico/Bike ao final!")
