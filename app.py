import streamlit as st
from audio_recorder_streamlit import audio_recorder
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
from io import BytesIO
import tempfile

# Supported languages
langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

def main():

    st.title("PragyanAI - VVIET Workshop: Audio Hub")

    # Optional image
    try:
        st.image("virat-kohli-hd-mrf-bat-iwsd28t8xsmz9b9b.jpg")
    except:
        st.warning("Image file not found")

    # Record audio
    audio_bytes = audio_recorder(
        text="Click to record",
        neutral_color="#6aa36f"
    )

    if audio_bytes:

        st.audio(audio_bytes, format="audio/wav")

        # Language selection
        target_lang = st.selectbox(
            "Select Target Language",
            list(langs_dict.keys())
        )

        target_code = langs_dict[target_lang]

        if st.button("Process & Translate"):

            try:
                # Save audio temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(audio_bytes)
                    temp_audio_path = tmp_file.name

                # Speech Recognition
                recognizer = sr.Recognizer()

                with sr.AudioFile(temp_audio_path) as source:
                    audio_data = recognizer.record(source)

                text = recognizer.recognize_google(audio_data)

                st.success(f"Original: {text}")

                # Translation
                translated_text = GoogleTranslator(
                    source='auto',
                    target=target_code
                ).translate(text)

                st.info(f"Translated: {translated_text}")

                # Text to Speech
                tts = gTTS(
                    text=translated_text,
                    lang=target_code
                )

                tts_fp = BytesIO()
                tts.write_to_fp(tts_fp)

                st.audio(tts_fp.getvalue(), format="audio/mp3")

            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
