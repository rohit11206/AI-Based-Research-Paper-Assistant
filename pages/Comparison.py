import streamlit as st
import os
from langchain_groq import ChatGroq
import fitz  # PyMuPDF
from dotenv import load_dotenv
from shared.ui import inject_custom_css, render_hero

load_dotenv()

# -----------------------------
# 🔹 Load LLM (Groq)
# -----------------------------
def load_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing")
    return ChatGroq(
        api_key=api_key,
        model="llama-3.1-8b-instant"
    )

# -----------------------------
# 🔹 Extract text from PDF
# -----------------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


# -----------------------------
# 🔹 Summarize paper
# -----------------------------
def summarize_paper(text, llm):
    prompt = f"""
    Summarize this research paper in a concise way:

    {text[:4000]}
    """
    response = llm.invoke(prompt)
    return response.content


# -----------------------------
# 🔹 Compare papers
# -----------------------------
def compare_papers(summaries, llm):
    combined = "\n\n".join(
        [f"Paper {i+1}:\n{s}" for i, s in enumerate(summaries)]
    )

    prompt = f"""
    Compare the following research papers:

    {combined}

    Provide:
    1. Key Differences
    2. Methods Used
    3. Results Comparison
    4. Advantages and Disadvantages
    5. Final Conclusion

    Format output clearly with headings.
    """

    response = llm.invoke(prompt)
    return response.content


# -----------------------------
# 🔹 UI
# -----------------------------
st.set_page_config(page_title="Paper Comparison", layout="wide")
inject_custom_css()

render_hero(
    "Research Paper Comparison",
    "Upload multiple papers and get a structured side-by-side analysis.",
    chips=["Summaries", "Methods", "Results"],
)

st.markdown('<div class="app-card">', unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_files and len(uploaded_files) < 2:
    st.warning("⚠️ Please upload at least 2 papers")

if uploaded_files and len(uploaded_files) >= 2:
    if not os.getenv("GROQ_API_KEY"):
        st.error(
            "GROQ_API_KEY not found. Add it to your `.env` file, then restart Streamlit."
        )
        st.code("GROQ_API_KEY=your_key_here")

    if st.button("🚀 Compare Papers"):
        try:
            with st.spinner("Processing papers..."):
                llm = load_llm()

                texts = []
                summaries = []

                # Step 1: Extract text
                for file in uploaded_files:
                    text = extract_text_from_pdf(file)
                    texts.append(text)

                # Step 2: Summarize each paper
                for i, text in enumerate(texts):
                    st.write(f"🔹 Summarizing Paper {i+1}...")
                    summary = summarize_paper(text, llm)
                    summaries.append(summary)

                # Step 3: Compare
                st.write("🔍 Comparing papers...")
                result = compare_papers(summaries, llm)

            # Output
            st.success("✅ Comparison Complete!")
            st.markdown("## 📊 Comparison Result")
            st.write(result)
        except Exception as e:
            st.error(f"Comparison failed: {str(e)}")