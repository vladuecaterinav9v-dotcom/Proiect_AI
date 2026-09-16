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

# 5. Funcție avansată adaptată special pentru LinkedIn cu tonuri net diferite
def genereaza_continut_linkedin(subiect, tip, ton, hashtags, emojis, cheie, rol):
    context_rol = f" (în calitate de {rol})" if rol else ""

    # Fiecare ton are un stil de scriere și o structură complet diferită
    if ton == "Profesional & Analitic":
        emo = "📊 " if emojis else ""
        titlu = f"{emo}**ANALIZĂ DE IMPACT: Modul în care inovația schimbă regulile**\n\n"
        intro_p = f"Analizând evoluția recentă legată de **{subiect}**{context_rol}, observăm o nevoie clară de eficientizare și optimizare în industrie.\n\n"
        body_p = (
            "📈 **3 Constatări Analitice Cheie:**\n"
            "• **Optimizarea proceselor:** Reducerea timpului de execuție prin automatizare inteligentă.\n"
            "• **Decizii bazate pe date:** Eliminarea presupunerilor și focalizarea pe metrice concrete.\n"
            "• **Scalabilitate:** Construirea unei baze solide pentru creștere pe termen lung.\n\n"
            "Concluzia? Adaptarea rapidă la noile tehnologii este singurul avantaj competitiv sustenabil."
        )
        cta_p = "\n\n💬 **Care este metrica principală pe care o urmărești în proiectele tale? Aștept părerea ta în comentarii.**"

    elif ton == "Corporate":
        emo = "🏢 " if emojis else ""
        titlu = f"{emo}**ANUNȚ OFICIAL | Dezvoltare & Inovație**\n\n"
        intro_p = f"Suntem încântați să împărtășim o nouă etapă importantă în activitatea noastră: **{subiect}**{context_rol}.\n\n"
        body_p = (
            "Atingerea acestui obiectiv confirmă angajamentul nostru pentru excelență și profesionalism. "
            "Rezultatele obținute reflectă efortul continuu și alinierea la cele mai înalte standarde din industrie.\n\n"
            "Pilonii strategici ai acestei inițiative:\n"
            "1️⃣ **Standardizare:** Aliniere la bunele practici din domeniu.\n"
            "2️⃣ **Colaborare:** Integrare eficientă între resurse și tehnologie.\n"
            "3️⃣ **Sustenabilitate:** Impact pozitiv și valoare pe termen lung."
        )
        cta_p = "\n\n🤝 **Vă invităm să ne urmăriți pentru viitoare noutăți și oportunități de colaborare.**"

    elif ton == "Motivațional & Leadership":
        emo = "🚀 " if emojis else ""
        titlu = f"{emo}**Succesul nu este o întâmplare, ci o alegere zilnică!**\n\n"
        intro_p = f"Când am început lucrul la **{subiect}**{context_rol}, am înțeles că cele mai mari provocări aduc cele mai valoroase lecții.\n\n"
        body_p = (
            "Nu este vorba doar despre rezultatul final, ci despre cine devii pe parcurs! 🔥\n\n"
            "✨ **3 Lecții de leadership învățate pe parcurs:**\n"
            "• **Pasiune & Perseverență:** Nimic nu înlocuiește munca consecventă.\n"
            "• **Depășirea limitelor:** Zona de confort este inamicul progresului.\n"
            "• **Învățare continuă:** Fiecare eroare este doar un pas spre soluția corectă."
        )
        cta_p = "\n\n👇 **Care a fost cea mai mare provocare pe care ai transformat-o într-o reușită anul acesta? Lasă un comentariu!**"

    else:  # Academic & Tehnic
        emo = "💡 " if emojis else ""
        titlu = f"{emo}**[TECHNICAL CASE STUDY] Arhitectură & Implementare**\n\n"
        intro_p = f"Prezentare tehnică referitoare la implementarea proiectului: **{subiect}**{context_rol}.\n\n"
        body_p = (
            "⚙️ **Detalii Arhitecturale & Stack Tehnologic:**\n"
            "• **Core:** Design modular axat pe performanță și timp de răspuns minim.\n"
            "• **Procesare:** Algoritmi optimizați pentru manipularea eficientă a datelor.\n"
            "• **UX/UI:** Interfață reactivă, complet decuplată de logica de backend.\n\n"
            "🔍 **Rezultat tehnic:** Optimizarea fluxului de date și asigurarea unei execuții stabile în mediu de producție."
        )
        cta_p = "\n\n🛠️ **Pentru întrebări legate de arhitectură sau detalii de implementare, vă stau la dispoziție.**"

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
                    st.markdown("### 🖼️ Imagine Corporate AI (Fotorealistă):")
                    
                    # Prompt optimizat pentru fotorealism extrem
                    prompt_fotorealist = (
                        f"A real realistic photograph of {subiect}, professional office environment, "
                        f"authentic corporate setting, shot on 35mm lens, f/2.8 aperture, soft natural lighting, "
                        f"DSLR camera quality, highly detailed, photorealistic, cinematic depth of field"
                    )
                    prompt_encoded = urllib.parse.quote(prompt_fotorealist)
                    
                    # Generare cu modelul Flux pentru calitate fotorealistă
                    image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=800&height=800&nologo=true&model=flux"
                    
                    st.image(image_url, caption="Imagine fotorealistă generată de AI (Model: Flux)", use_container_width=True)

# Footer
st.markdown("---")
st.caption("Proiect realizat în Python & Streamlit | Facultatea de Automatică și Calculatoare")