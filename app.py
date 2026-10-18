import streamlit as st
import requests

# --- Configuration de la page (Style iMessage) ---
st.set_page_config(page_title="iMessage Multi-Agents", page_icon="💬", layout="centered")

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
    .agent-tag {
        font-size: 11px; color: #8e8e93; margin-bottom: 2px; font-weight: 600; text-transform: uppercase;
        clear: both; float: left;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialisation de la clé API en session ---
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# --- 🧠 BARRE LATÉRALE : MÉMOIRE & CLÉ API ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    user_api_input = st.text_input("Clé API Groq (gsk_...)", type="password", value=st.session_state.api_key)
    if user_api_input:
        st.session_state.api_key = user_api_input
    
    st.divider()
    st.header("🧠 Mémoire Globale (Profil)")
    user_nom = st.text_input("Ton Prénom / Pseudo", value="Développeur")
    user_niveau = st.text_input("Niveau / Rôle", value="Étudiant / Autodidacte")
    user_objectifs = st.text_area("Objectifs & Projets", value="Créer un chat multi-agents et des applications sur iPad.")
    
    st.divider()
    if st.button("🗑️ Effacer la discussion"):
        st.session_state.messages = []
        st.rerun()

st.title("💬 iMessage Multi-Agents")

# --- Initialisation de l'historique ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div style="display: flex; justify-content: flex-end;"><div class="user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="agent-tag">{msg["agent"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="display: flex; justify-content: flex-start;"><div class="ai-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)

# --- Fonction pour appeler Groq avec un Rôle d'Agent spécifique ---
def appeler_agent_groq(prompt, agent_role, profil_utilisateur, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    system_prompt = f"""
    Tu es un assistant virtuel intelligent au sein d'une équipe multi-agents inspirée des meilleures IA du marché.
    Voici le profil de la personne à qui tu parles :
    - Nom : {profil_utilisateur['nom']}
    - Niveau : {profil_utilisateur['niveau']}
    - Objectifs : {profil_utilisateur['objectifs']}
    
    Ton rôle spécifique actuel : {agent_role}
    Réponds toujours en tenant compte de ce profil, de manière claire, structurée et adaptée.
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ Erreur API ({response.status_code}) : {response.text}"
    except Exception as e:
        return f"❌ Erreur de connexion : {e}"

# --- Le Routeur Intelligent (Spécialisé par IA de ta liste) ---
def router_requete(prompt):
    p = prompt.lower()
    if any(kw in p for kw in ["traduis", "traduction", "anglais", "espagnol", "deepl", "formule"]):
        return "🌐 Agent DeepL (Traduction)", "Un expert incontesté de la traduction de documents et de la reformulation/amélioration de style."
    elif any(kw in p for kw in ["code", "html", "python", "site", "bug", "script", "développe", "cursor"]):
        return "💻 Agent Cursor (Code)", "Un assistant de programmation/codage pour écrire, corriger et compléter du code proprement."
    elif any(kw in p for kw in ["cherche", "actualité", "infos", "sur internet", "qui est", "perplexity"]):
        return "🔍 Agent Perplexity (Recherche)", "Le roi de la recherche sourcée, agissant comme un moteur de recherche intelligent."
    elif any(kw in p for kw in ["rédige", "lettre", "texte", "article", "claude", "histoire", "analyse"]):
        return "✍️ Agent Claude (Rédaction)", "Le meilleur pour la qualité de l'écriture, l'analyse de documents complexes et le raisonnement nuancé."
    elif any(kw in p for kw in ["image", "dessine", "illustration", "leonardo"]):
        return "🎨 Agent Leonardo.ai (Création visuelle)", "Un agent spécialisé pour décrire, concevoir et structurer des prompts pour la génération d'images artistiques."
    else:
        return "🧠 Agent ChatGPT (Polyvalent)", "Le plus polyvalent pour la conversation, la rédaction, le résumé et la recherche générale."

# --- Zone de saisie du chat ---
if prompt := st.chat_input("iMessage..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    if not st.session_state.api_key:
        nom_agent = "⚠️ Système"
        reponse = "Veuillez entrer votre clé API Groq dans la barre latérale !"
    else:
        nom_agent, role_description = router_requete(prompt)
        
        profil = {
            "nom": user_nom,
            "niveau": user_niveau,
            "objectifs": user_objectifs
        }
        
        with st.spinner(f"{nom_agent} prend le relais..."):
            reponse = appeler_agent_groq(prompt, role_description, profil, st.session_state.api_key)
            
    st.session_state.messages.append({"role": "assistant", "agent": nom_agent, "content": reponse})
    st.rerun()
