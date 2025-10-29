import streamlit as st
import random
import time

st.set_page_config(page_title="Meus Jogos", page_icon="🎮", layout="centered")

# Inicializa variáveis
for var, default in {
    "tela": "menu",
    "jogador_atual": 1,
    "nome1": "",
    "nome2": "",
    "pontos1": 0,
    "pontos2": 0,
    "contador_perguntas": 0,
    "perguntas_embaralhadas": []
}.items():
    if var not in st.session_state:
        st.session_state[var] = default

if "mostrar_mensagem_hot" not in st.session_state:
    st.session_state.mostrar_mensagem_hot = False

# Função de retorno ao menu principal
def voltar_menu():
    # Resetar variáveis principais
    st.session_state.tela = "menu"
    st.session_state.jogador_atual = 1
    st.session_state.pontos1 = 0
    st.session_state.pontos2 = 0
    st.session_state.contador_perguntas = 0
    st.session_state.nome1 = ""
    st.session_state.nome2 = ""
    st.session_state.perguntas_embaralhadas = []

    # Resetar modo do quiz, se existir
    if "modo_quiz" in st.session_state:
        del st.session_state["modo_quiz"]

def tela_menu():
    st.title("🎮 Menu de Jogos")
    st.write("Escolha um jogo para começar:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Dado Sexy", use_container_width=True):
            st.session_state.tela = "dado"
    with col2:
        if st.button("🎯 Quiz do casal", use_container_width=True):
            st.session_state.tela = "quiz"

def tela_dado():
    st.header("🎲 Dado Sexy")
    slot = st.empty()
    if st.button("CLIQUE AQUI", key="dado_btn"):
        delay = 0.05
        for i in range(15):
            numero_temp = random.randint(1, 6)
            slot.image(f"Img/dado{numero_temp}.png", width=500)
            time.sleep(delay)
            delay += 0.03
        numero_final = random.randint(1, 22)
        slot.image(f"Img/{numero_final}.png", width=500)
    else:
        slot.image("Img/inicio.png", width=500)
    st.button("🏠 Voltar ao Menu", on_click=voltar_menu)

def tela_quiz():
    # Pausa para exibir mensagem HOT após erro
    if st.session_state.get("mostrar_mensagem_hot", False):
        nome_atual = st.session_state.nome1 if st.session_state.jogador_atual == 1 else st.session_state.nome2
        st.markdown(f"""<div style="color: red; font-size: 26px; font-weight: bold; border: 3px solid white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 0 15px white; background-color: black;">
            <h3>❌ {nome_atual} Errou!</h3>
            <p><strong>Tire uma peça de roupa.</strong></p>
            <p>🔥 Modo HOT ativado 🔥</p>
        </div>""", unsafe_allow_html=True)

        if st.button("OK, continuar"):
            st.session_state.mostrar_mensagem_hot = False
            st.session_state.contador_perguntas += 1
            st.session_state.jogador_atual = 2 if st.session_state.jogador_atual == 1 else 1
            st.rerun()
        return  # ⚠️ Interrompe o restante da função até clicar OK

    
    # Seleção de modo via botões
    if "modo_quiz" not in st.session_state:
        st.subheader("Escolha o tipo de quiz:")
        if st.button("💑 Quiz Casal"):
            st.session_state.modo_quiz = "casal"
            st.rerun()
        if st.button("🔥 Quiz Hot"):
            st.session_state.modo_quiz = "hot"
            st.rerun()

        return
    if st.session_state.modo_quiz == "casal":
        titulo_quiz = "💑 Quiz do Casal"
    else:
        titulo_quiz = "🔥 Quiz Hot"
    st.header(titulo_quiz)

    # Define o arquivo com base no modo escolhido
    arquivo_quiz = "quiz_casal.txt" if st.session_state.modo_quiz == "casal" else "quiz_hot.txt"


    if st.session_state.nome1 == "" or st.session_state.nome2 == "":
        with st.form("form_nomes"):
            nome1 = st.text_input("Nome do Jogador 1:")
            nome2 = st.text_input("Nome do Jogador 2:")
            col1, col2 = st.columns(2)
            with col1:
                iniciar = st.form_submit_button("✅ Começar")
            with col2:
                voltar = st.form_submit_button("🏠 Voltar ao Menu")

        if iniciar:
            if nome1.strip() and nome2.strip():
                st.session_state.nome1 = nome1.strip()
                st.session_state.nome2 = nome2.strip()
                st.rerun()
        else:
            st.warning("⚠️ Preencha os dois nomes antes de começar o quiz.")
        # ⚠️ Interrompe o restante da função até que os nomes sejam definidos
        return
    if not st.session_state.perguntas_embaralhadas:
        try:
            with open(arquivo_quiz, "r", encoding="utf-8") as f:
                perguntas = [linha.strip() for linha in f if linha.strip()]
            random.shuffle(perguntas)
            st.session_state.perguntas_embaralhadas = perguntas[:20]
        except FileNotFoundError:
            st.error(f"❌ Arquivo {arquivo_quiz} não encontrado.")
            st.button("🏠 Voltar ao Menu", on_click=voltar_menu)
            return

    if st.session_state.contador_perguntas >= len(st.session_state.perguntas_embaralhadas):
        st.markdown("## 🏁 Fim do jogo!")
        st.markdown(f"{st.session_state.nome1}: {st.session_state.pontos1} ponto(s)")
        st.markdown(f"**{st.session_state.nome2}**: {st.session_state.pontos2} ponto(s)")
        vencedor = (
            st.session_state.nome1 if st.session_state.pontos1 > st.session_state.pontos2
            else st.session_state.nome2 if st.session_state.pontos2 > st.session_state.pontos1
            else "Empate!"
        )
        st.success(f"🎉 Vencedor: {vencedor}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Jogar novamente"):
                st.session_state.pontos1 = 0
                st.session_state.pontos2 = 0
                st.session_state.contador_perguntas = 0
                st.session_state.perguntas_embaralhadas = []
                st.rerun()
        with col2:
            st.button("🏠 Voltar ao Menu", on_click=voltar_menu)
        return

    pergunta = st.session_state.perguntas_embaralhadas[st.session_state.contador_perguntas]
    st.markdown(
        f"""<div style="color: red; font-size: 26px; font-weight: bold;
        border: 3px solid white; padding: 20px; border-radius: 12px;
        text-align: center; box-shadow: 0 0 15px white; background-color: black;">
        {pergunta}</div>""",
        unsafe_allow_html=True
    )

    nome_atual = st.session_state.nome1 if st.session_state.jogador_atual == 1 else st.session_state.nome2
    st.subheader(f"👤 Jogador da vez a responder: {nome_atual}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Acertou"):
            if st.session_state.jogador_atual == 1:
                st.session_state.pontos1 += 1
            else:
                st.session_state.pontos2 += 1
            st.session_state.contador_perguntas += 1
            st.session_state.jogador_atual = 2 if st.session_state.jogador_atual == 1 else 1
            st.rerun()
        if st.button("❌ Errou"):
            if st.session_state.modo_quiz == "hot":
                st.session_state.mostrar_mensagem_hot = True
            else:
                st.session_state.contador_perguntas += 1
                st.session_state.jogador_atual = 2 if st.session_state.jogador_atual == 1 else 1
                st.rerun()


    with col2:
        st.button("🏠 Voltar ao Menu", on_click=voltar_menu)

    st.markdown("---")
    st.markdown(f"🏆 **{st.session_state.nome1}**: {st.session_state.pontos1} ponto(s)")
    st.markdown(f"🏆 **{st.session_state.nome2}**: {st.session_state.pontos2} ponto(s)")
    st.markdown(f"📊 Perguntas respondidas: {st.session_state.contador_perguntas}/20")

# Chamada da tela correta
if st.session_state.tela == "menu":
    tela_menu()
elif st.session_state.tela == "dado":
    tela_dado()
elif st.session_state.tela == "quiz":
    tela_quiz()
