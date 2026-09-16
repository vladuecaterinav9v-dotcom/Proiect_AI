# Proiect Practică - Generator AI Postări LinkedIn

Aplicația este creată în Python cu Streamlit și ajută la generarea de postări pentru LinkedIn și la crearea de imagini potrivite.

---

## Cum am scris codul (pas cu pas):

1. **Importul librăriilor:**  
   Am încărcat mai întâi librăriile necesare: `streamlit` pentru interfața grafică, `urllib.parse` pentru construirea link-ului de imagine și `dotenv` pentru configurarea proiectului.

2. **Configurarea paginii și meniului:**  
   Am setat titlul aplicației și am creat un sidebar (`st.sidebar`) în stânga. Acolo am adăugat opțiunile de selectat: formatul postării, un slider pentru tonul vorbirii și bifat pentru hashtag-uri sau imagine.

3. **Zona de introducere date:**  
   În pagina principală am pus o casetă mare de text unde utilizatorul își scrie ideea sau proiectul, plus două casete mai mici pentru rolul său și cuvintele cheie.

4. **Logica de generare text (`genereaza_continut_linkedin`):**  
   Am creat o funcție care conține un dicționar cu fraze gata pregătite pentru fiecare ton (Corporate, Motivațional, Tehnic, Analitic). Funcția ia textul scris de utilizator, îl combină cu frazele potrivite din dicționar și creează postarea structurată. Tot aici am făcut codul care ia cuvintele cheie și le transformă în hashtag-uri.

5. **Generarea imaginii cu AI:**  
   Am folosit `urllib.parse.quote` ca să transform descrierea introducă într-un text sigur pentru un link web. Am trimis acest text către API-ul gratuit Pollinations AI, care generează o imagine de tip birou/corporate de 800x800 pixeli.

6. **Afișarea și butonul de postare:**  
   Când se apasă butonul de generare, am împărțit ecranul în două coloane (`st.columns`): în stânga apare textul generat cu un buton care deschide direct LinkedIn, iar în dreapta se încarcă imaginea AI.
