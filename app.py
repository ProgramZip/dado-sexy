import streamlit as st
import random
import time

st.set_page_config(page_title="Dado Sexy", page_icon="🎲", layout="centered")

st.title("🎲 Dado Sexy")

# Espaço reservado para a imagem
slot = st.empty()

# Criar um botão que exibe a imagem inicial
if st.button("CLIQUE AQUI", key="dado_btn"):
    # Animação: mostrar apenas as faces 1 a 6
    delay = 0.05
    for i in range(15):
        numero_temp = random.randint(1, 6)  # só usa dado1.png até dado6.png
        slot.image(f"Img/dado{numero_temp}.png", width=500)
        time.sleep(delay)
        delay += 0.03  # desacelera

    # Resultado final: sorteio entre 1 e 22
    numero_final = random.randint(1, 22)
    slot.image(f"Img/{numero_final}.png", width=500)
else:
    # Imagem inicial (serve como "botão visual")
    slot.image("Img/inicio.png", width=500)
