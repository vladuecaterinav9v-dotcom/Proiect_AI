import streamlit as st
import os
import urllib.parse
from dotenv import load_dotenv

# 1. Configurare pagină
load_dotenv()
st.set_page_config(page_title="Social Media AI Generator", page_icon="🎨", layout="wide")

# 2. Titlu
st.title("📲 Generator AI: Text Extins & Imagini Social Media")
st.caption("Proiect de practică - Facultatea de Automatică și Calculatoare")
st.markdown("---")

# 3. Meniu Lateral
st.sidebar.header("⚙️ Setări Conținut")

tip_continut = st.sidebar.selectbox(
    "Formatul dorit:",
    ["Postare Facebook", "Story Instagram (3 Cadre)", "Postare LinkedIn", "Caption TikTok / Reel"]
)

ton_voce = st.sidebar.select_slider(
    "Tonul vorbirii:",
    options=["Profesional", "Informativ", "Prietenos / Entuziast", "Amuzant", "Inspirațional"]
)

include_hashtags = st.sidebar.checkbox("Hashtag-uri inteligente", value=True)
include_emojis = st.sidebar.checkbox("Include Emoji-uri", value=True)
generare_imagine = st.sidebar.checkbox("Generează Imagine AI", value=True)

# 4. Zona de Introducere Subiect
st.subheader("1. Despre ce este postarea?")
subiect = st.text_area(
    "Descrie pe scurt ideea, produsul sau evenimentul:",
    placeholder="Exemplu: Târgul de Crăciun din Craiova - luminițe spectaculoase, patinoar și ciocolată caldă...",
    height=90
)

cuvinte_cheie = st.text_input("Locație / Cuvinte cheie suplimentare (Opțional):", placeholder="Ex: Craiova, Crăciun, Magie")

# 5. Funcție avansată de generare cu adaptare reală a tonului și text extins
def genereaza_continut_avansat(subiect, tip, ton, hashtags, emojis, cheie):
    # Dicționar de stiluri dinamice în funcție de TON
    stiluri_ton = {
        "Profesional": {
            "hook": "Anunț important și oportunitate deosebită:",
            "intro": "Avem plăcerea de a vă aduce în atenție o experiență de referință:",
            "tranzit": "Printre elementele definitorii ale acestei inițiative se numără:",
            "cta": "Vă invităm să consultați detaliile complete și să vă alăturați acestei experiențe.",
            "emo_prefix": "💼 " if emojis else ""
        },
        "Informativ": {
            "hook": "Ghid util & Detalii esențiale:",
            "intro": "Tot ce trebuie să știi în acest moment despre următoarea recomandare:",
            "tranzit": "Iată reperele principale pe care trebuie să le iei în calcul:",
            "cta": "Salvează această postare pentru a avea la îndemână toate informațiile utile!",
            "emo_prefix": "📌 " if emojis else ""
        },
        "Prietenos / Entuziast": {
            "hook": "Pregătește-te de ceva cu adevărat special! 🎉",
            "intro": "Nu mai putem ține secretul! Trebuia neapărat să împărtășim asta cu voi:",
            "tranzit": "Iată ce ne încântă cel mai tare și de ce nu trebuie să ratezi așa ceva:",
            "cta": "Etichetează în comentarii persoana cu care vrei să mergi neapărat!",
            "emo_prefix": "🚀 " if emojis else ""
        },
        "Amuzant": {
            "hook": "Ai spus că stai acasă weekendul ăsta? Mai gândește-te o dată! 😂",
            "intro": "Avem planul perfect care o să-ți dea peste cap toate scuzele de a nu ieși din casă:",
            "tranzit": "Motivele oficiale pentru care merită să lași canapeaua deoparte:",
            "cta": "Lasă un comentariu dacă și tu ai nevoie de o pauză memorabilă!",
            "emo_prefix": "😎 " if emojis else ""
        },
        "Inspirațional": {
            "hook": "Momentele speciale sunt cele pe care le păstrăm în suflet. ✨",
            "intro": "Există locuri și momente care reușesc să transforme o simplă zi într-o amintire de poveste:",
            "tranzit": "Frumusețea acestei experiențe constă în detalii unice:",
            "cta": "Bucură-te de fiecare clipă și creează-ți propriile amintiri speciale.",
            "emo_prefix": "🌟 " if emojis else ""
        }
    }

    s = stiluri_ton[ton]
    e = s["emo_prefix"]

    if tip == "Story Instagram (3 Cadre)":
        rezultat = f"""
📸 **CADRUL 1 (Atenție & Titlu):**
{e}{s['hook']}
👉 {s['intro']}
Swipe up / Glisează pentru detalii!

📸 **CADRUL 2 (Experiență & Detalii Extinse):**
{'✨ ' if emojis else ''}{subiect}
{s['tranzit']}
• Atmosferă de neuitat și momente unice
• Activități concepute special pentru public
• Trăiri pe care merită să le experimentezi în direct!

📸 **CADRUL 3 (Call to Action & Interacțiune):**
{'🎯 ' if emojis else ''}{s['cta']}
Ești gata? Trimite un mesaj privat sau răspunde la acest Story!
        """
    else:
        # Descriere extinsă pentru Facebook / LinkedIn / TikTok
        titlu = f"{e}**{s['hook']}**\n\n"
        intro_paragraph = f"{s['intro']}\n👉 **{subiect}**\n\n"
        
        body_paragraph = (
            f"{s['tranzit']}\n"
            f"• **Atmosferă & Design:** O organizare atentă, gândită să creeze o experiență vizuală și emoțională deosebită.\n"
            f"• **Puncte de interes:** Fiecare detaliu a fost conceput pentru a oferi momente memorabile tuturor vizitatorilor.\n"
            f"• **Nivel de energie:** Un mediu ideal pentru a te deconecta, a socializa și a te bucura de tot ce este mai frumos.\n\n"
            f"Această inițiativă își propune să aducă împreună comunitatea și să ofere un spațiu de conectare autentică. Fiecare vizită devine astfel o poveste de neuitat."
        )
        
        cta_paragraph = f"\n\n💬 **{s['cta']}**"
        
        rezultat = titlu + intro_paragraph + body_paragraph + cta_paragraph

    # Hashtag-uri dinamice
    tags_text = ""
    if hashtags:
        cuvinte_importante = [w.strip(",.!?").capitalize() for w in subiect.split() if len(w) > 3]
        custom_tags = [f"#{ck.strip().replace(' ', '')}" for ck in cheie.split(",") if ck.strip()]
        
        tags_generat = [f"#{w}" for w in cuvinte_importante[:5]] + custom_tags + ["#Romania", "#SocialMedia", "#Trending", "#InstaGood"]
        tags_text = "\n\n🏷️ **Hashtag-uri relevante:**\n" + " ".join(list(set(tags_generat))[:8])

    return rezultat, tags_text

# 6. Generare & Afișare
st.markdown("---")
if st.button("✨ Generează Postarea Extinsă & Imaginea AI", type="primary", use_container_width=True):
    if not subiect.strip():
        st.warning("⚠️ Te rog să scrii mai întâi un scurt subiect!")
    else:
        with st.spinner("AI-ul adaptează tonul și generează conținutul extins..."):
            text_generat, tags = genereaza_continut_avansat(subiect, tip_continut, ton_voce, include_hashtags, include_emojis, cuvinte_cheie)
            
            st.success(f"✅ Postare generată cu stilul: {ton_voce}!")
            
            # Afișare pe 2 coloane
            col_text, col_img = st.columns([3, 2])
            
            with col_text:
                st.markdown("### 📝 Text Generat Extins:")
                st.code(text_generat, language="text")
                if tags:
                    st.markdown(tags)

            with col_img:
                if generare_imagine:
                    st.markdown("### 🖼️ Imagine AI Generată:")
                    prompt_encoded = urllib.parse.quote(f"{subiect}, highly detailed, cinematic lighting, photorealistic, 8k resolution")
                    image_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=800&height=800&nologo=true"
                    
                    st.image(image_url, caption="Imagine creată în timp real de AI", use_container_width=True)

# Footer
st.markdown("---")
st.caption("Proiect realizat în Python & Streamlit | Facultatea de Automatică și Calculatoare")