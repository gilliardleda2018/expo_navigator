import os
import io
import streamlit as st

QUESTIONS = [
    ("Aeroporto", "Onde fica o píer da Alilaguna?", "Scusi, dov'è il molo dei trasporti via acqua per Alilaguna?"),
    ("Aeroporto", "Onde compro o bilhete para Veneza?", "Dove posso comprare il biglietto per Venezia?"),
    ("Aeroporto", "Este transporte vai até o centro de Veneza?", "Questo mezzo arriva al centro di Venezia?"),
    ("Barco", "Qual linha devo pegar?", "Quale linea devo prendere?"),
    ("Barco", "Onde fica a parada mais próxima?", "Dov'è la fermata più vicina?"),
    ("Barco", "Este barco vai para Rialto?", "Questo vaporetto va a Rialto?"),
    ("Hospedagem", "Como chego a este endereço?", "Come posso arrivare a questo indirizzo?"),
    ("Hospedagem", "Posso deixar minha bagagem aqui?", "Posso lasciare qui il mio bagaglio?"),
    ("Hospedagem", "A que horas posso fazer o check-in?", "A che ora posso fare il check-in?"),
    ("Segurança", "Preciso de ajuda, por favor.", "Ho bisogno di aiuto, per favore."),
    ("Segurança", "Onde fica a farmácia mais próxima?", "Dov'è la farmacia più vicina?"),
    ("Segurança", "Pode chamar um táxi aquático?", "Può chiamare un taxi acqueo, per favore?"),
]

st.set_page_config(page_title="Expo Navigator | Veneza", page_icon="🇮🇹", layout="centered")
st.title("🇮🇹 Áudios estratégicos")
st.caption("12 perguntas essenciais para aeroporto, barco, hospedagem e segurança.")

def api_key():
    try:
        return st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    except Exception:
        return os.getenv("OPENAI_API_KEY")

@st.cache_resource
def client(key):
    from openai import OpenAI
    return OpenAI(api_key=key)

def synthesize(text, language):
    result = client(api_key()).audio.speech.create(model="tts-1", voice="alloy", input=text)
    return result.content

def transcribe(blob):
    audio = io.BytesIO(blob)
    audio.name = "resposta.wav"
    result = client(api_key()).audio.transcriptions.create(model="whisper-1", file=audio, language="it")
    return result.text

def translate(text):
    response = client(api_key()).chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Traduza fielmente do italiano para português brasileiro. Responda apenas com a tradução."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""

key = api_key()
if not key:
    st.warning("Configure OPENAI_API_KEY para habilitar áudio, transcrição e tradução.")

for idx, (category, question, italian) in enumerate(QUESTIONS):
    with st.container(border=True):
        st.caption(category)
        st.subheader(question)
        st.write(italian)
        if st.button("🔊 Ouvir pergunta em italiano", key=f"say_{idx}", disabled=not key):
            try:
                st.audio(synthesize(italian, "it"), format="audio/mp3")
            except Exception as exc:
                st.error(f"Não foi possível gerar o áudio: {exc}")
        st.write("**Resposta do atendente**")
        st.caption("Toque no microfone para gravar. Ao encerrar, a transcrição será iniciada automaticamente.")
        recording = st.audio_input("🎙️ Gravar resposta", key=f"record_{idx}", disabled=not key)
        audio_bytes = recording.getvalue() if recording else None
        fingerprint = __import__("hashlib").sha256(audio_bytes).hexdigest() if audio_bytes else None
        marker = f"processed_{idx}"
        text_key = f"italian_{idx}"
        translation_key = f"portuguese_{idx}"
        if fingerprint and st.session_state.get(marker) != fingerprint:
            try:
                with st.spinner("Transcrevendo resposta em italiano..."):
                    recognized = transcribe(audio_bytes)
                st.session_state[text_key] = recognized
                st.session_state[translation_key] = ""
                st.session_state[marker] = fingerprint
            except Exception as exc:
                st.error(f"Falha na transcrição: {exc}. Você pode digitar a resposta.")
        st.text_area("Resposta em italiano", key=text_key, placeholder="Transcrição automática ou digite aqui")
        if st.button("🇧🇷 Traduzir e gerar áudio", key=f"translate_{idx}", disabled=not key or not st.session_state.get(text_key, "").strip()):
            try:
                with st.spinner("Traduzindo..."):
                    st.session_state[translation_key] = translate(st.session_state[text_key])
            except Exception as exc:
                st.error(f"Não foi possível traduzir: {exc}")
        if st.session_state.get(translation_key):
            st.text_area("Tradução em português", value=st.session_state[translation_key], disabled=True, key=f"output_{idx}")
            if st.button("🔊 Ouvir tradução", key=f"play_{idx}", disabled=not key):
                try:
                    st.audio(synthesize(st.session_state[translation_key], "pt"), format="audio/mp3")
                except Exception as exc:
                    st.error(f"Não foi possível gerar o áudio: {exc}")
