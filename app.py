import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Read API key from Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("models/gemini-3.5-flash")

st.title("📄 Paper to Presentation & Viva Agent")

uploaded_file = st.file_uploader(
    "Upload Research Paper PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    try:
        pdf = PdfReader(uploaded_file)

        text = ""

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

        st.success("PDF Uploaded Successfully")

        if st.button("Generate"):

            with st.spinner("Generating Results..."):

                summary = model.generate_content(
                    f"Summarize this research paper:\n{text[:20000]}"
                )

                slides = model.generate_content(
                    f"Create a 10-slide presentation from this paper:\n{text[:20000]}"
                )

                viva = model.generate_content(
                    f"Generate 20 viva questions with answers from this paper:\n{text[:20000]}"
                )

            st.subheader("Research Paper Summary")
            st.write(summary.text)

            st.subheader("Presentation Slides")
            st.write(slides.text)

            st.subheader("Viva Questions and Answers")
            st.write(viva.text)

    except Exception as e:
        st.error(str(e))