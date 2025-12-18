import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd
from docx import Document
import pdfplumber
from io import BytesIO

# ======================================
# KONFIGURASI HALAMAN
# ======================================
st.set_page_config(
    page_title="Aplikasi Translator by Nurul",
    layout="wide"
)

# ======================================
# STYLE CSS (PINK LEMBUT)
# ======================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #ffe6f0, #fff5fa);
}
.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
.title {
    font-size: 36px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ======================================
# SIDEBAR
# ======================================
with st.sidebar:
    st.markdown("## 💗 Aplikasi Translator")
    st.write(
        "Terjemahkan teks dan dokumen dari "
        "**Bahasa Indonesia ↔ Inggris** dengan mudah."
    )
    st.markdown("---")
    st.write("👩‍💻 Dibuat oleh **Nurul**")

# ======================================
# HEADER
# ======================================
st.markdown('<div class="title">🌐 Aplikasi Translator by Nurul</div>', unsafe_allow_html=True)
st.write("")

# ======================================
# LAYOUT
# ======================================
col1, col2 = st.columns([1, 2])

# ======================================
# INPUT KIRI
# ======================================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    mode = st.selectbox(
        "Pilih Arah Terjemahan",
        ["Indonesia ke Inggris", "Inggris ke Indonesia"]
    )

    input_type = st.radio(
        "Jenis Input",
        ["Input Teks Manual", "Upload File"]
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ======================================
# INPUT KANAN
# ======================================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    text = ""

    if input_type == "Input Teks Manual":
        text = st.text_area("Masukkan teks", height=220)

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
                text = "\n".join(p.text for p in doc.paragraphs)

            elif uploaded_file.name.endswith(".pdf"):
                with pdfplumber.open(uploaded_file) as pdf:
                    pages = [
                        page.extract_text()
                        for page in pdf.pages
                        if page.extract_text()
                    ]
                    text = "\n".join(pages)

            st.text_area("Isi dokumen", text, height=220)

    st.markdown('</div>', unsafe_allow_html=True)

# ======================================
# TRANSLATE
# ======================================
st.write("")
if st.button("🔁 Translate"):
    if not text.strip():
        st.warning("⚠️ Teks masih kosong")
    else:
        translator = GoogleTranslator(
            source="id" if mode == "Indonesia ke Inggris" else "en",
            target="en" if mode == "Indonesia ke Inggris" else "id"
        )

        # POTONG TEKS (ANTI ERROR 5000 CHAR)
        MAX_CHARS = 4500
        chunks = [
            text[i:i + MAX_CHARS]
            for i in range(0, len(text), MAX_CHARS)
        ]

        translated_text = ""
        for chunk in chunks:
            translated_text += translator.translate(chunk) + "\n"

        # TAMPILKAN HASIL
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.text_area("Hasil Terjemahan", translated_text, height=250)

        # SIMPAN KE WORD
        doc = Document()
        for line in translated_text.split("\n"):
            doc.add_paragraph(line)

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            "⬇️ Download Hasil (.docx)",
            buffer,
            file_name="hasil_translate.docx"
        )

        st.markdown('</div>', unsafe_allow_html=True)
