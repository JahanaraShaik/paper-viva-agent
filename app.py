import streamlit as st
from pypdf import PdfReader
import requests
import io

try:
    from google import genai
except Exception:
    st.error("Please install: python -m pip install google-genai")
    st.stop()

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Paper to Presentation & Viva Agent",
    page_icon="📚",
    layout="wide"
)

# -----------------------------------
# HEADER
# -----------------------------------

try:
    st.image("assets/cmr_logo.png", width=250)
except:
    pass

st.title("📚 Paper to Presentation & Viva Agent")

st.markdown("""
### AI-Powered Research Assistant

Upload a research paper PDF or provide a paper URL.

Features:

✅ Detailed Summary

✅ Main Contributions

✅ Research Impact

✅ Presentation Slides

✅ Viva Questions

✅ Research Gaps

✅ Future Work

✅ Paper Expert Agent
""")

try:
    st.image("assets/research.png", use_container_width=True)
except:
    pass

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.header("🔑 Settings")

api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password"
)

client = None

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        st.sidebar.success("API Key Loaded Successfully")
    except Exception as e:
        st.sidebar.error(str(e))

# -----------------------------------
# PAPER INPUT
# -----------------------------------

paper_url = st.text_input(
    "Research Paper URL (Optional)"
)

uploaded_file = st.file_uploader(
    "Upload Research Paper PDF",
    type=["pdf"]
)

if paper_url:
    try:
        response = requests.get(
            paper_url,
            timeout=15
        )

        if response.status_code == 200:
            uploaded_file = io.BytesIO(response.content)
            st.success("Paper downloaded successfully")
        else:
            st.error(
                "Unable to access paper. Please upload PDF."
            )

    except Exception:
        st.error(
            "Unable to access paper. Please upload PDF."
        )

# -----------------------------------
# PAPER ANALYSIS
# -----------------------------------

if uploaded_file is not None and client:

    try:
        pdf = PdfReader(uploaded_file)

        text = ""

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

        st.success("Paper Loaded Successfully")

        st.session_state["paper_text"] = text

        if st.button("Generate Analysis"):

            with st.spinner("Analyzing Paper..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"""
Analyze this research paper and provide:

1. Detailed Summary
2. Main Contributions
3. Novelty
4. Research Impact
5. Professional 10 Slide Presentation
6. 20 Viva Questions with Answers
7. Research Gaps
8. Limitations
9. Future Work
10. Extension Ideas

Paper:

{text[:12000]}
"""
                )

                st.subheader("📖 Research Paper Analysis")
                st.write(response.text)

    except Exception as e:
        st.error(str(e))

# -----------------------------------
# PAPER EXPERT AGENT
# -----------------------------------

if "paper_text" in st.session_state and client:

    st.divider()

    st.header("🤖 Paper Expert Agent")

    recommended_questions = [
        "Explain this paper in simple language",
        "What are the main contributions?",
        "What are the limitations?",
        "What research gaps exist?",
        "How can I extend this work?",
        "Generate viva questions",
        "What future work is possible?",
        "What questions might an examiner ask?"
    ]

    selected = st.selectbox(
        "Recommended Questions",
        recommended_questions
    )

    question = st.text_input(
        "Ask Anything About The Paper",
        value=selected
    )

    if st.button("Ask Agent"):

        with st.spinner("Thinking..."):

            answer = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
Research Paper:

{st.session_state['paper_text'][:12000]}

Question:

{question}

Give a detailed answer.
"""
            )

            st.write(answer.text)

st.divider()

st.caption(
    "Developed for Research Presentation and Viva Preparation"
)