import streamlit as st
from shared.ui import inject_custom_css, render_hero

st.set_page_config(page_title="IEEE Paper Constructor", layout="wide")
inject_custom_css()

from constructor.github_loader import parse_repo, fetch_repo, _check_rate_limit, _headers
from constructor.vectorstore import build_vectorstore
from constructor.analysis import analyze_repository
from constructor.paper_generator import generate_paper
from constructor.pdf_builder import build_pdf

render_hero(
    "IEEE Research Paper Constructor",
    "Convert a GitHub repository into a structured IEEE-style draft paper.",
    chips=["GitHub Analysis", "Auto Draft", "PDF Export"],
)

# Show GitHub API rate limit status in sidebar
with st.sidebar:
    st.subheader("GitHub API Status")
    rate_limit = _check_rate_limit(_headers())
    if rate_limit:
        if rate_limit["status"] == "ok":
            st.success(f"✅ API Remaining: {rate_limit['remaining']}/{rate_limit['limit']}")
        else:
            st.warning(f"⚠️ API Low: {rate_limit['remaining']}/{rate_limit['limit']}")
            st.info(f"Resets at: {rate_limit['reset_time']}")
    st.caption("Without GITHUB_TOKEN: 60 req/hour\nWith GITHUB_TOKEN: 5000 req/hour")

if "sections" not in st.session_state:
    st.session_state.sections = None
if "repo_name" not in st.session_state:
    st.session_state.repo_name = ""
if "author" not in st.session_state:
    st.session_state.author = ""
if "institution" not in st.session_state:
    st.session_state.institution = ""

with st.container():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    with st.form("constructor_form"):
        repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/owner/repository")
        col1, col2 = st.columns(2)
        with col1:
            author = st.text_input("Author Name", placeholder="John Doe")
        with col2:
            institution = st.text_input("Institution", placeholder="Your University / Organization")
        submit = st.form_submit_button("Generate Paper")
    st.markdown("</div>", unsafe_allow_html=True)

if submit:
    st.session_state.author = author
    st.session_state.institution = institution

    owner, repo = parse_repo(repo_url)
    if not owner:
        st.error("Invalid GitHub URL")
        st.stop()

    try:
        with st.spinner("Fetching repository..."):
            repo_data = fetch_repo(owner, repo, max_files=40)

        with st.spinner("Building vector database..."):
            vector_db = build_vectorstore(repo_data)

        with st.spinner("Analyzing repository..."):
            analysis = analyze_repository(repo_data)

        with st.spinner("Generating paper..."):
            sections = generate_paper(repo_data, analysis, vector_db)

        st.session_state.sections = sections
        st.session_state.repo_name = repo
        
    except RuntimeError as e:
        st.error(f"Error: {str(e)}")
        st.stop()
    st.markdown(st.session_state.sections.get("abstract", ""))

    pdf = build_pdf(
        st.session_state.sections,
        st.session_state.author,
        st.session_state.institution,
    )

    st.download_button(
        "Download PDF",
        pdf.getvalue(),
        file_name=f"{st.session_state.repo_name}_ieee_paper.pdf",
        mime="application/pdf",
    )
