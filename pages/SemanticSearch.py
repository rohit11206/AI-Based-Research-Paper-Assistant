import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import feedparser
from urllib.parse import quote
import re
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


def lexical_overlap_score(query_text, title, abstract):
    """Simple keyword relevance score in [0, 1]."""
    query_tokens = tokenize(query_text)
    if not query_tokens:
        return 0.0
    doc_tokens = tokenize(f"{title} {abstract}")
    overlap = len(query_tokens.intersection(doc_tokens))
    return overlap / len(query_tokens)

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
query = st.text_input("Enter your research topic", placeholder="e.g., transformer interpretability in NLP")

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

    if query.strip() == "":
        st.warning("⚠️ Please enter a query")
    
    else:
        with st.spinner("Fetching and analyzing papers..."):
            # Step 1: Fetch papers
            papers = fetch_arxiv_papers(query, max_results=120)

            if len(papers) == 0:
                st.error("No papers found")
            
            else:
                # Step 2: Prepare text (boost title importance)
                texts = [
                    (p["title"] + " ") * 2 + p["abstract"]
                    for p in papers
                ]

                # Step 3: Embeddings
                paper_embeddings = model.encode(texts)
                query_embedding = model.encode([query])

                # Step 4: Similarity + lexical relevance (hybrid ranking)
                semantic_scores = cosine_similarity(query_embedding, paper_embeddings)[0]
                lexical_scores = np.array(
                    [lexical_overlap_score(query, p["title"], p["abstract"]) for p in papers]
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

                # Fallback: if strict filtering removes all, show top-N with warning.
                if shown_count < min_results:
                    st.warning(
                        "Not enough papers passed the relevance threshold. "
                        "Showing best available matches below."
                    )
                    for i in top_indices[:min_results]:
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