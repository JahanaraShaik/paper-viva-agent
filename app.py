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

st.title("📄 Paper to Presentation & Viva Agent V2")

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

                summary = model.generate_content(
                    f"""
                    Summarize this research paper in detail.

                    Paper:
                    {text[:15000]}
                    """
                )

                contributions = model.generate_content(
                    f"""
                    Identify:

                    1. Main Contributions
                    2. Novelty
                    3. Importance
                    4. Research Impact

                    Paper:
                    {text[:15000]}
                    """
                )

                slides = model.generate_content(
                    f"""
                    Create a professional 10-slide presentation.

                    Paper:
                    {text[:15000]}
                    """
                )

                viva = model.generate_content(
                    f"""
                    Generate 20 viva questions with answers.

                    Paper:
                    {text[:15000]}
                    """
                )

                gaps = model.generate_content(
                    f"""
                    Identify:

                    1. Research Gaps
                    2. Limitations
                    3. Future Work
                    4. Extension Ideas

                    Paper:
                    {text[:15000]}
                    """
                )

            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "Summary",
                "Contributions",
                "Slides",
                "Viva",
                "Research Gaps"
            ])

            with tab1:
                st.write(summary.text)

            with tab2:
                st.write(contributions.text)

            with tab3:
                st.write(slides.text)

            with tab4:
                st.write(viva.text)

            with tab5:
                st.write(gaps.text)

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

        if question:

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