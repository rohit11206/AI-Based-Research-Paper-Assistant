import streamlit as st
from shared.ui import inject_custom_css

st.set_page_config(
    page_title="Research Paper Assistant",
    layout="wide",
)

inject_custom_css()


def go_to(page_path: str):
    if hasattr(st, "switch_page"):
        st.switch_page(page_path)
    else:
        st.info("Use the left sidebar to open pages.")

st.markdown(
    """
    <div class="landing-nav">
        <div class="landing-brand"><span class="landing-brand-dot">●</span>Research Assistant</div>
        <div class="landing-right">AI-Powered Research Workflow</div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.25, 1], gap="large")

with left:
    st.markdown(
        """
        <div class="landing-hero-left">
            <h1>Your All-in-One <span class="landing-highlight">AI Research Assistant</span></h1>
        </div>
        <div class="landing-sub">
            Find related papers, compare 2 or more papers, ask questions on PDFs, and generate IEEE-style drafts from repositories in one clean workspace.
        </div>
        <div class="landing-feature"><span class="landing-feature-icon">✓</span>Question-based semantic search with relevance ranking</div>
        <div class="landing-feature"><span class="landing-feature-icon">✓</span>Compare 2 or more research papers with key differences and conclusions</div>
        <div class="landing-feature"><span class="landing-feature-icon">✓</span>Document Q&A with memory across chat sessions</div>
        <div class="landing-feature"><span class="landing-feature-icon">✓</span>Automated paper construction and PDF export</div>
        """,
        unsafe_allow_html=True,
    )

    cta1, cta2, cta3, cta4 = st.columns(4)
    with cta1:
        if st.button("Open Constructor", use_container_width=True):
            go_to("pages/Constructor.py")
    with cta2:
        if st.button("Open Deconstructor", use_container_width=True):
            go_to("pages/Deconstructor.py")
    with cta3:
        if st.button("Semantic Search", use_container_width=True):
            go_to("pages/SemanticSearch.py")
    with cta4:
        if st.button("Compare Papers", use_container_width=True):
            go_to("pages/Comparison.py")

with right:
    st.markdown(
        """
        <div class="mock-card">
            <div class="mock-search">Ask your research question</div>
            <div class="mock-pill">5,900 Journals Fetched</div>
            <div class="mock-pill">46,000 Papers Analyzed</div>
            <p style="margin: .4rem 0 .55rem 0; color:#334155; font-weight:600;">Analysis from top 10 papers:</p>
            <div class="mock-line long"></div>
            <div class="mock-line mid"></div>
            <div class="mock-line long"></div>
            <div class="mock-line short"></div>
            <div class="mock-line mid"></div>
            <div style="margin-top:.65rem;">
                <span class="mock-pill">Meta-Analysis</span>
                <span class="mock-pill">Top Journal</span>
                <span class="mock-pill">Cited</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
st.caption("Use the blue buttons above to start quickly.")
