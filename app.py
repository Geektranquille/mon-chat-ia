import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Mon iMessage AI", page_icon="💬", layout="centered")

# Style visuel iMessage (Bulles bleues et grises)
st.markdown("""
<style>
    .stApp { background-color: #f2f2f7; }
    .user-bubble {
        background-color: #007aff; color: white;
        border-radius: 18px 18px 4px 18px; padding: 10px 16px;
        max-width: 70%; font-size: 15px; margin-bottom: 8px;
        float: right; clear: both;
    }
    .ai-bubble {
        background-color: #e5e5ea; color: black;
        border-radius: 18px 18px 18px 4px; padding: 10px 16px;
        max-width: 70%; font-size: 15px; margin-bottom: 8px;
        float: left; clear: both;
    }
</style>
""", unsafe_allow_html=True)

st.title("💬 iMessage AI")

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div style="display: flex; justify-content: flex-end;"><div class="user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="display: flex; justify-content: flex-start;"><div class="ai-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)

# Zone de saisie du chat
if prompt := st.chat_input("iMessage..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    reponse_test = f"J'ai bien reçu : '{prompt}'. L'étape 1 fonctionne !"
    st.session_state.messages.append({"role": "assistant", "content": reponse_test})
    st.rerun()
