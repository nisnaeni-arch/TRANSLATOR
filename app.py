import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd
from docx import Document
import pdfplumber

# ===============================
# KONFIGURASI HALAMAN
# ===============================
st.set_page_config(
    page_title="Translator by Nurul",
    layout="centered"
)

st.title("🌐 Aplikasi Translate Indonesia ↔ Inggris")

# ===============================
# FUNGSI UNTUK TEKS PANJANG
# ===============================
def translate_long_text(translator, text, chunk_size=4000):
    """
    Memecah teks panjang menjadi beberapa bagian
    untuk menghindari batas 5000 karakter GoogleTranslator
    """
    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]

    translated_chunks = []
    for chunk in chunks:
        translated_chunks.append(translator.translate(chunk))

    return " ".join(translated_chunks)

# ===============================
# PILIH MODE TRANSLASI
# ===============================
mode = st.selectbox(
    "Pilih Arah Terjemahan",
    ["Indonesia ke Inggris", "Inggris ke Indonesia"]
)

# ===============================
# PILIH JENIS INPUT
# ===============================
input_type = st.radio(
    "Pilih Jenis Input",
    ["Input Teks Manual", "Upload File"]
)

text = ""

# ===============================
# INPUT MANUAL
# ===============================
if input_type == "Input Teks Manual":
    text = st.text_area(
        "Masukkan teks",
        height=200
    )

# ===============================
# UPLOAD FILE
# ===============================
else:
    uploaded_file = st.file_uploader(
        "Upload file (.txt, .csv, .docx, .pdf)",
        type=["txt", "csv", "docx", "pdf"]
    )

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")

        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            text = " ".join(df.astype(str).values.flatten())

        elif uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            text = "\n".join(
                p.text for p in doc.paragraphs if p.text.strip()
            )

        elif uploaded_file.name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                pages_text = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages_text.append(page_text)
                text = "\n".join(pages_text)

        st.text_area(
            "Isi teks dari file",
            text,
            height=200
        )

# ===============================
# PROSES TRANSLATE
# ===============================
if st.button("🔁 Translate"):
    if text.strip() == "":
        st.warning("⚠️ Teks kosong, silakan masukkan teks.")
    else:
        with st.spinner("⏳ Sedang menerjemahkan..."):
            if mode == "Indonesia ke Inggris":
                translator = GoogleTranslator(source="id", target="en")
            else:
                translator = GoogleTranslator(source="en", target="id")

            try:
                result = translate_long_text(translator, text)

                st.text_area(
                    "Hasil Terjemahan",
                    result,
                    height=200
                )

                st.download_button(
                    "⬇️ Download Hasil",
                    result,
                    file_name="hasil_translate.txt"
                )

            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {e}")
