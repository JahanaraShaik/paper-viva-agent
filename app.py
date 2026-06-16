import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("models/gemini-3.5-flash")

st.set_page_config(
    page_title="Paper to Presentation & Viva Agent",
    layout="wide"
)

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

        st.session_state["paper_text"] = text

        if st.button("Generate Analysis"):

            with st.spinner("Analyzing Paper..."):

                result = model.generate_content(
                    f"""
                    Analyze the following research paper and provide:

                    1. Detailed Summary

                    2. Main Contributions

                    3. Novelty and Research Impact

                    4. Professional 10 Slide Presentation

                    5. 20 Viva Questions with Answers

                    6. Research Gaps

                    7. Limitations

                    8. Future Work

                    9. Extension Ideas

                    Research Paper:

                    {text[:15000]}
                    """
                )

                st.subheader("Complete Research Analysis")

                st.write(result.text)

    except Exception as e:
        st.error(str(e))

# Paper Expert Agent

if "paper_text" in st.session_state:

    st.divider()

    st.header("🤖 Paper Expert Agent")

    question = st.text_input(
        "Ask anything about the paper"
    )

    if st.button("Ask Agent"):

        with st.spinner("Thinking..."):

            answer = model.generate_content(
                f"""
                Research Paper:

                {st.session_state['paper_text'][:15000]}

                User Question:

                {question}

                Give a detailed answer.
                """
            )

            st.write(answer.text)