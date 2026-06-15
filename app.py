import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# Gemini API
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

if uploaded_file:

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    st.success("PDF Uploaded Successfully")

    st.session_state["paper_text"] = text

    if st.button("Generate Complete Analysis"):

        with st.spinner("Analyzing Paper... Please Wait"):

            summary = model.generate_content(
                f"Summarize this research paper:\n{text[:20000]}"
            )

            contributions = model.generate_content(
                f"""
                Analyze this paper and provide:

                1. Main Contributions
                2. Novel Contributions
                3. Importance of the Work
                4. Research Impact

                Paper:
                {text[:20000]}
                """
            )

            slides = model.generate_content(
                f"""
                Create a professional 10-slide presentation.

                Paper:
                {text[:20000]}
                """
            )

            speaker_notes = model.generate_content(
                f"""
                Create speaker notes for each presentation slide.

                Explain:
                - What to say
                - Key discussion points
                - Presentation tips

                Paper:
                {text[:20000]}
                """
            )

            viva = model.generate_content(
                f"""
                Generate 20 viva questions with detailed answers.

                Paper:
                {text[:20000]}
                """
            )

            gaps = model.generate_content(
                f"""
                Identify:

                1. Research Gaps
                2. Limitations
                3. Future Scope
                4. Publishable Extension Ideas

                Paper:
                {text[:20000]}
                """
            )

            literature = model.generate_content(
                f"""
                Create a literature review summary.

                Include:
                - Background
                - Related Work
                - Research Trends

                Paper:
                {text[:20000]}
                """
            )

            citations = model.generate_content(
                f"""
                Generate:

                1. APA Citation
                2. IEEE Citation
                3. BibTeX Entry

                Paper:
                {text[:5000]}
                """
            )

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Summary",
            "Contributions",
            "Slides",
            "Speaker Notes",
            "Viva",
            "Research Gaps",
            "Literature & Citations"
        ])

        with tab1:
            st.write(summary.text)

        with tab2:
            st.write(contributions.text)

        with tab3:
            st.write(slides.text)

        with tab4:
            st.write(speaker_notes.text)

        with tab5:
            st.write(viva.text)

        with tab6:
            st.write(gaps.text)

        with tab7:
            st.subheader("Literature Review")
            st.write(literature.text)

            st.subheader("Citations")
            st.write(citations.text)

# Paper Expert Agent
if "paper_text" in st.session_state:

    st.divider()

    st.header("🤖 Paper Expert Agent")

    question = st.text_input(
        "Ask anything about the uploaded paper"
    )

    if st.button("Ask Agent"):

        with st.spinner("Thinking..."):

            answer = model.generate_content(
                f"""
                Research Paper:

                {st.session_state['paper_text'][:20000]}

                User Question:

                {question}

                Give a detailed answer.
                """
            )

        st.write(answer.text)