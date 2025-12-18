import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd
from docx import Document
import pdfplumber

st.set_page_config(page_title="Translator ID ↔ EN", layout="centered")
st.title("🌐 Aplikasi Translate Indonesia ↔ Inggris")

mode = st.selectbox(
    "Pilih Arah Terjemahan",
    ["Indonesia ke Inggris", "Inggris ke Indonesia"]
)

input_type = st.radio(
    "Pilih Jenis Input",
    ["Input Teks Manual", "Upload File"]
)

text = ""

if input_type == "Input Teks Manual":
    text = st.text_area("Masukkan teks", height=200)
else:
    uploaded_file = st.file_uploader(
        "Upload file (.txt, .csv, .docx, .pdf)",
        type=["txt", "csv", "docx", "pdf"]
    )

    if uploaded_file:
        if uploaded_file.name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            text = " ".join(df.astype(str).values.flatten())
        elif uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            text = "\n".join([p.text for p in doc.paragraphs])
        elif uploaded_file.name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join(
                    page.extract_text()
                    for page in pdf.pages
                    if page.extract_text()
                )

        st.text_area("Isi teks dari file", text, height=200)

if st.button("🔁 Translate"):
    if text.strip() == "":
        st.warning("⚠️ Teks kosong")
    else:
        if mode == "Indonesia ke Inggris":
            translator = GoogleTranslator(source="id", target="en")
        else:
            translator = GoogleTranslator(source="en", target="id")

        result = translator.translate(text)
        st.text_area("Hasil Terjemahan", result, height=200)
        st.download_button(
            "⬇️ Download Hasil",
            result,
            file_name="hasil_translate.txt"
        )

