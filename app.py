import streamlit as st
import os
import urllib.parse
from dotenv import load_dotenv

# 1. Configurare pagină
load_dotenv()
st.set_page_config(page_title="LinkedIn AI Assistant", page_icon="💼", layout="wide")

# 2. Titlu
st.title("💼 Generator AI: Postări & Imagini LinkedIn (Pro)")
st.caption("Proiect de practică - Facultatea de Automatică și Calculatoare")
st.markdown("---")

# 3. Meniu Lateral
st.sidebar.header("⚙️ Setări Conținut LinkedIn")

tip_continut = st.sidebar.selectbox(
    "Formatul postării:",
    [
        "Opinie despre industrie (Thought Leadership)",
        "Realizare profesională / Certificare",
        "Anunț de angajare / Recrutare",
        "Studiu de caz / Prezentare Proiect"
    ]
)

ton_voce = st.sidebar.select_slider(
    "Tonul vorbirii:",
    options=["Profesional & Analitic", "Corporate", "Motivațional & Leadership", "Academic & Tehnic"]
)

include_hashtags = st.sidebar.checkbox("Hashtag-uri profesionale", value=True)
include_emojis = st.sidebar.checkbox("Include Emoji-uri de business", value=True)
generare_imagine = st.sidebar.checkbox("Generează Imagine Corporate AI", value=True)

# 4. Zona de Introducere Subiect
st.subheader("1. Detalii despre postarea de LinkedIn")

col_input1, col_input2 = st.columns([2, 1])

with col_input1:
    subiect = st.text_area(
        "Descrie pe scurt subiectul, ideea sau realizarea ta:",
        placeholder="Exemplu: Am finalizat un proiect de inteligență artificială care optimizează postările pentru social media folosind Streamlit și Python...",
        height=100
    )

with col_input2:
    rol_companie = st.text_input("Rolul tău / Domeniul (Opțional):", placeholder="Ex: Student Automatică / Data Scientist")
    cuvinte_cheie = st.text_input("Cuvinte cheie / Tehnologii (Opțional):", placeholder="Ex: Python, AI, Streamlit, Innovation")

# 5. Funcție avansată adaptată special pentru LinkedIn
def genereaza_continut_linkedin(subiect, tip, ton, hashtags, emojis, cheie, rol):
    stiluri_ton = {
        "Profesional & Analitic": {
            "hook": "O perspectivă valoroasă asupra modului în care evoluează domeniul nostru:",
            "intro": "Analizând tendințele actuale, devine clar că inovația redefinește standardele din industrie.",
            "tranzit": "Iată 3 concluzii principale pe care le putem extrage:",
            "cta": "Care este opinia ta despre această abordare? Aștept cu interes ideile tale în comentarii.",
            "emo_prefix": "📊 " if emojis else ""
        },
        "Corporate": {
            "hook": "Ne bucurăm să împărtășim o nouă etapă importantă în activitatea noastră:",
            "intro": "Dedicarea și strategia sunt motoarele principale ale unei dezvoltări sustenabile.",
            "tranzit": "Elementele cheie care au contribuit la acest rezultat:",
            "cta": "Vă invităm să urmăriți evoluția proiectului și să ne conectați pentru viitoare colaborări.",
            "emo_prefix": "🏢 " if emojis else ""
        },
        "Motivațional & Leadership": {
            "hook": "Succesul nu este o destinație, ci un proces continuu de învățare și adaptare.",
            "intro": "Fiecare provocare întâlnită în proiecte reprezintă o oportunitate de creștere profesională.",
            "tranzit": "Lecțiile principale pe care le-am învățat pe parcurs:",
            "cta": "Tu ce provocare ai transformat recent într-o oportunitate? Lasă un comentariu mai jos!",
            "emo_prefix": "🚀 " if emojis else ""
        },
        "Academic & Tehnic": {
            "hook": "Studiu de caz tehnic & Implementare practică:",
            "intro": "Soluțiile moderne necesită o arhitectură bine structurată și utilizarea eficientă a tehnologiilor actuale.",
            "tranzit": "Aspecte tehnice definitorii ale implementării:",
            "cta": "Pentru mai multe detalii tehnice sau întrebări despre arhitectură, vă stau la dispoziție.",
            "emo_prefix": "💡 " if emojis else ""
        }
    }

    s = stiluri_ton[ton]
    e = s["emo_prefix"]
    context_rol = f" Din perspectiva unui **{rol}**:" if rol else ""

    # Construcție structură postare LinkedIn
    titlu = f"{e}**{s['hook']}**\n\n"
    intro_p = f"{s['intro']}{context_rol}\n\n📌 **Context:** {subiect}\n\n"
    
    body_p = (
        f"**{s['tranzit']}**\n"
        f"1. **Eficiență & Structură:** Focus pe soluții scalabile și rezultate concrete.\n"
        f"2. **Implementare Practică:** Utilizarea celor mai bune practici din industrie.\n"
        f"3. **Impact & Valoare:** Crearea de valoare adăugată pentru utilizatori și comunitate.\n\n"
        f"Această abordare demonstrează importanța adaptării continue la noile cerințe din mediul profesional."
    )
    
    cta_p = f"\n\n💬 **{s['cta']}**"
    
    rezultat = titlu + intro_p + body_p + cta_p

    # Hashtag-uri specifice LinkedIn
    tags_text = ""
    if hashtags:
        custom_tags = [f"#{ck.strip().replace(' ', '')}" for ck in cheie.split(",") if ck.strip()]
        tags_generat = custom_tags + ["#LinkedIn", "#Business", "#Leadership", "#CareerGrowth", "#Innovation", "#TechIndustry"]
        tags_text = "\n\n🏷️ **Hashtag-uri LinkedIn:**\n" + " ".join(list(set(tags_generat))[:8])

    return rezultat, tags_text

# 6. Generare & Afișare
st.markdown("---")
if st.button("🚀 Generează Postare LinkedIn & Imagine Corporate", type="primary", use_container_width=True):
    if not subiect.strip():
        st.warning("⚠️ Te rog să introduci detalii despre subiectul postării!")
    else:
        with st.spinner("AI-ul redactează postarea profesională pentru LinkedIn..."):
            text_generat, tags = genereaza_continut_linkedin(
                subiect, tip_continut, ton_voce, include_hashtags, include_emojis, cuvinte_cheie, rol_companie
            )
            
            st.success(f"✅ Postare optimizată pentru LinkedIn cu stilul: {ton_voce}!")
            
            col_text, col_img = st.columns([3, 2])
            
            with col_text:
                st.markdown("### 📝 Text Generat pentru LinkedIn:")
                st.code(text_generat, language="text")
                if tags:
                    st.markdown(tags)
                
                # Varianta 2: Buton direct de Share / Deschidere LinkedIn
                st.markdown("---")
                st.link_button("🌐 Deschide LinkedIn & Postează", "https://www.linkedin.com/feed/", use_container_width=True)
                st.caption("💡 Apasă butonul de copiere din colțul casetei de text, deschide LinkedIn cu butonul de mai sus și dă Paste (Ctrl+V)!")

            with col_img:
                if generare_imagine:
                    st.markdown("### 🖼️ Imagine Corporate AI:")
                    # Prompt ajustat pentru stil profesional / business / office
                    prompt_encoded = urllib.parse.quote(
                        f"professional business concept, corporate office, modern workspace, {subiect}, clean design, high quality, photorealistic, 8k resolution"
                    )
                    image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=800&height=800&nologo=true"
                    
                    st.image(image_url, caption="Imagine profesională creată de AI", use_container_width=True)

# Footer
st.markdown("---")
st.caption("Proiect realizat în Python & Streamlit | Facultatea de Automatică și Calculatoare")