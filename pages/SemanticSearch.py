import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import feedparser
from urllib.parse import quote
import re
import fitz  # PyMuPDF
from shared.ui import inject_custom_css, render_hero

# -----------------------------
# 🔹 Load Model
# -----------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()


def tokenize(text):
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "have", "has", "are", "was",
    "were", "into", "using", "use", "used", "based", "paper", "research", "study",
    "method", "methods", "results", "analysis", "proposed", "approach", "model",
    "system", "data", "dataset", "our", "their", "its", "can", "will", "also", "than",
}


def lexical_overlap_score(query_text, title, abstract):
    """Simple keyword relevance score in [0, 1]."""
    query_tokens = tokenize(query_text)
    if not query_tokens:
        return 0.0
    doc_tokens = tokenize(f"{title} {abstract}")
    overlap = len(query_tokens.intersection(doc_tokens))
    return overlap / len(query_tokens)


def extract_text_from_pdf_bytes(pdf_bytes):
    text_parts = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        max_pages = min(len(doc), 4)
        for page_idx in range(max_pages):
            text_parts.append(doc[page_idx].get_text())
    return " ".join(text_parts)


def build_query_from_text(raw_text, max_terms=14):
    """
    Create a concise keyword query from long paper text.
    Long raw text in arXiv `all:` search often returns zero results.
    """
    tokens = re.findall(r"[a-zA-Z]{3,}", raw_text.lower())
    freq = {}
    for token in tokens:
        if token in STOPWORDS:
            continue
        freq[token] = freq.get(token, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [w for w, _ in ranked[:max_terms]]
    return " ".join(keywords)


def extract_query_from_paper_url(paper_url):
    """Try to convert a paper URL into a useful search query."""
    url = paper_url.strip()

    # arXiv URL support: https://arxiv.org/abs/xxxx or /pdf/xxxx.pdf
    match = re.search(r"arxiv\.org/(abs|pdf)/([^/?#]+)", url)
    if match:
        arxiv_id = match.group(2).replace(".pdf", "")
        arxiv_api = (
            "http://export.arxiv.org/api/query?search_query=id:"
            f"{quote(arxiv_id)}&start=0&max_results=1"
        )
        feed = feedparser.parse(arxiv_api)
        if feed.entries:
            entry = feed.entries[0]
            return f"{entry.title} {entry.summary[:1000]}"

    # Generic fallback: use readable URL slug words
    slug = re.sub(r"https?://", "", url).split("/")[-1]
    slug = re.sub(r"[-_]+", " ", slug)
    slug = re.sub(r"\.[a-zA-Z0-9]+$", "", slug)
    return slug.strip()

# -----------------------------
# 🔹 Fetch Papers from arXiv (Improved)
# -----------------------------
def fetch_arxiv_papers(query, max_results=100):
    encoded_query = quote(query)

    # Search in title + abstract (better relevance)
    url = (
        f"http://export.arxiv.org/api/query?"
        f"search_query=all:{encoded_query}&start=0&max_results={max_results}"
    )
    
    feed = feedparser.parse(url)
    
    papers = []
    
    for entry in feed.entries:
        papers.append({
            "title": entry.title,
            "abstract": entry.summary,
            "link": entry.link
        })
    
    return papers


def fetch_arxiv_with_fallback(primary_query):
    """Try primary query first, then a simplified one."""
    papers = fetch_arxiv_papers(primary_query, max_results=120)
    if papers:
        return papers, primary_query

    simplified_query = build_query_from_text(primary_query, max_terms=10)
    if simplified_query:
        papers = fetch_arxiv_papers(simplified_query, max_results=120)
        if papers:
            return papers, simplified_query
    return [], primary_query

# -----------------------------
# 🔹 UI
# -----------------------------
st.set_page_config(page_title="Semantic Search", layout="wide")
inject_custom_css()

render_hero(
    "Semantic Search",
    "Find the most relevant research papers by semantic similarity.",
    chips=["arXiv", "Similarity Ranking", "Topic Discovery"],
)

st.markdown('<div class="app-card">', unsafe_allow_html=True)
search_mode = st.radio(
    "Search input type",
    ["Topic Query", "Upload PDF", "Paper Link"],
    horizontal=True,
)

query = ""
uploaded_pdf = None
paper_link = ""

if search_mode == "Topic Query":
    query = st.text_input(
        "Enter your research topic",
        placeholder="e.g., transformer interpretability in NLP",
    )
elif search_mode == "Upload PDF":
    uploaded_pdf = st.file_uploader("Upload one research paper (PDF)", type=["pdf"])
else:
    paper_link = st.text_input(
        "Paste research paper link",
        placeholder="e.g., https://arxiv.org/abs/1706.03762",
    )

col1, col2, col3 = st.columns(3)
with col1:
    base_threshold = st.slider("Base relevance threshold", 0.1, 0.8, 0.35, 0.05)
with col2:
    semantic_weight = st.slider("Semantic weight", 0.4, 0.95, 0.75, 0.05)
with col3:
    min_results = st.slider("Minimum results to show", 1, 10, 3, 1)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# 🔹 SEARCH
# -----------------------------
if st.button("Search"):
    try:
        if search_mode == "Topic Query":
            if query.strip() == "":
                st.warning("Please enter a topic query.")
                st.stop()
            search_query = query.strip()
        elif search_mode == "Upload PDF":
            if uploaded_pdf is None:
                st.warning("Please upload a PDF first.")
                st.stop()
            pdf_text = extract_text_from_pdf_bytes(uploaded_pdf.getvalue())
            if not pdf_text.strip():
                st.warning("Could not extract text from this PDF.")
                st.stop()
            search_query = build_query_from_text(pdf_text, max_terms=14)
            if not search_query:
                st.warning("Could not derive a useful query from this PDF.")
                st.stop()
            st.caption(f"Using derived query from PDF: {search_query}")
        else:
            if paper_link.strip() == "":
                st.warning("Please provide a paper link.")
                st.stop()
            search_query = extract_query_from_paper_url(paper_link)
            if not search_query:
                st.warning("Could not derive query terms from this link.")
                st.stop()
            st.caption(f"Using derived query: {search_query[:140]}...")

        with st.spinner("Fetching and analyzing papers..."):
            # Step 1: Fetch papers
            papers, used_query = fetch_arxiv_with_fallback(search_query)
            if used_query != search_query:
                st.caption(f"Using fallback query: {used_query}")

            if len(papers) == 0:
                st.error(
                    "No papers found for this input. Try a different paper, use Topic Query mode, or lower semantic weight."
                )
            
            else:
                # Step 2: Prepare text (boost title importance)
                texts = [
                    (p["title"] + " ") * 2 + p["abstract"]
                    for p in papers
                ]

                # Step 3: Embeddings
                paper_embeddings = model.encode(texts)
                query_embedding = model.encode([used_query])

                # Step 4: Similarity + lexical relevance (hybrid ranking)
                semantic_scores = cosine_similarity(query_embedding, paper_embeddings)[0]
                lexical_scores = np.array(
                    [lexical_overlap_score(used_query, p["title"], p["abstract"]) for p in papers]
                )
                hybrid_scores = (
                    semantic_weight * semantic_scores + (1 - semantic_weight) * lexical_scores
                )

                # Step 5: Get top results
                top_indices = np.argsort(hybrid_scores)[::-1]

                # Dynamic threshold: strict near top score, but never below base threshold.
                best_score = float(hybrid_scores[top_indices[0]])
                dynamic_threshold = max(base_threshold, best_score - 0.18)

                # -----------------------------
                # 🔹 DISPLAY RESULTS
                # -----------------------------
                st.markdown("## 📄 Top Related Papers")

                shown_count = 0
                shown_indices = set()

                for i in top_indices:
                    if hybrid_scores[i] < dynamic_threshold:
                        continue

                    paper = papers[i]
                    score = hybrid_scores[i]
                    sem_score = semantic_scores[i]
                    lex_score = lexical_scores[i]

                    st.markdown(f"### {paper['title']}")
                    st.write(
                        f"**Relevance Score:** {score:.2f} | "
                        f"Semantic: {sem_score:.2f} | Keyword: {lex_score:.2f}"
                    )
                    st.write(paper["abstract"])
                    st.markdown(f"[Read Paper]({paper['link']})")
                    st.write("---")
                    shown_count += 1
                    shown_indices.add(i)

                # Fallback: if strict filtering removes all, show top-N with warning.
                if shown_count < min_results:
                    st.warning(
                        "Not enough papers passed the relevance threshold. "
                        "Showing best available matches below."
                    )
                    needed = max(min_results - shown_count, 0)
                    for i in top_indices:
                        if needed == 0:
                            break
                        if i in shown_indices:
                            continue
                        paper = papers[i]
                        score = hybrid_scores[i]
                        sem_score = semantic_scores[i]
                        lex_score = lexical_scores[i]

                        st.markdown(f"### {paper['title']}")
                        st.write(
                            f"**Relevance Score:** {score:.2f} | "
                            f"Semantic: {sem_score:.2f} | Keyword: {lex_score:.2f}"
                        )
                        st.write(paper["abstract"])
                        st.markdown(f"[Read Paper]({paper['link']})")
                        st.write("---")
                        needed -= 1
    except Exception as e:
        st.error(f"Search failed: {str(e)}")