import streamlit as st
from typing import List, Optional

def inject_custom_css():
    """Inject global custom CSS for a clean light-mode UI."""
    st.markdown(
        """
        <style>
        :root {
            --app-bg: #f6f8fc;
            --surface: #ffffff;
            --surface-soft: #f8fafc;
            --border: #dbe3ef;
            --text: #0f172a;
            --muted: #52607a;
            --primary: #2563eb;
            --primary-strong: #1d4ed8;
            --shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        }

        .stApp {
            background: var(--app-bg);
            color: var(--text);
        }

        header, footer, .v-toolbar {visibility: hidden;}

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1180px;
        }

        h1, h2, h3, h4 {
            color: var(--text);
            letter-spacing: -0.02em;
        }

        p, span, label, .stMarkdown, .stCaption {
            color: var(--muted);
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--border);
        }

        .app-hero {
            border: 1px solid var(--border);
            background: linear-gradient(160deg, #ffffff 0%, #f8fbff 100%);
            box-shadow: var(--shadow);
            border-radius: 16px;
            padding: 1rem 1.25rem;
            margin: 0.5rem 0 1.25rem 0;
        }

        .app-card {
            border: 1px solid var(--border);
            background: var(--surface);
            border-radius: 14px;
            box-shadow: var(--shadow);
            padding: 1rem 1.1rem;
            margin-bottom: 0.9rem;
        }

        .app-chip {
            display: inline-block;
            border: 1px solid #bfdbfe;
            background: #eff6ff;
            color: #1e40af;
            border-radius: 999px;
            padding: 0.2rem 0.6rem;
            font-size: 0.78rem;
            margin-right: 0.3rem;
            margin-bottom: 0.3rem;
        }

        .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
            border-radius: 10px;
            border: 1px solid var(--border);
            background: var(--primary);
            color: #ffffff !important;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .stButton > button *, .stDownloadButton > button *, .stFormSubmitButton > button * {
            color: #ffffff !important;
            fill: #ffffff !important;
        }

        .stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
            background: var(--primary-strong);
            border-color: var(--primary-strong);
            transform: translateY(-1px);
        }

        .stButton > button:focus, .stDownloadButton > button:focus, .stFormSubmitButton > button:focus {
            color: #ffffff !important;
            border-color: var(--primary-strong);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
        }

        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox > div > div {
            border-radius: 10px;
            border: 1px solid var(--border);
            background: var(--surface);
        }

        [data-testid="stFileUploaderDropzone"] {
            border-radius: 12px;
            border: 1px dashed #93c5fd;
            background: #f8fbff;
        }

        [data-testid="stChatMessage"] {
            border: 1px solid var(--border);
            border-radius: 12px;
            background: #ffffff;
        }

        .landing-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 0.8rem 1rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow);
        }

        .landing-brand {
            font-size: 1.15rem;
            font-weight: 800;
            color: var(--text);
        }

        .landing-brand-dot {
            color: #fb923c;
            margin-right: 0.2rem;
        }

        .landing-right {
            color: var(--muted);
            font-size: 0.9rem;
            font-weight: 600;
        }

        .landing-hero-left h1 {
            font-size: 3rem;
            line-height: 1.1;
            margin-bottom: 0.75rem;
        }

        .landing-highlight {
            color: #f59e0b;
        }

        .landing-sub {
            font-size: 1.03rem;
            max-width: 720px;
            color: var(--muted);
            margin-bottom: 1.1rem;
        }

        .landing-feature {
            display: flex;
            align-items: start;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
            color: var(--text);
            font-size: 0.95rem;
        }

        .landing-feature-icon {
            color: #2563eb;
            font-weight: 800;
        }

        .mock-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: var(--shadow);
            padding: 1rem;
        }

        .mock-search {
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            padding: 0.55rem 0.7rem;
            color: #475569;
            margin-bottom: 0.8rem;
            font-size: 0.93rem;
        }

        .mock-pill {
            display: inline-block;
            background: #f0f9ff;
            border: 1px solid #bae6fd;
            border-radius: 999px;
            padding: 0.2rem 0.5rem;
            color: #075985;
            font-size: 0.75rem;
            margin-right: 0.3rem;
            margin-bottom: 0.35rem;
        }

        .mock-line {
            height: 10px;
            border-radius: 999px;
            background: #e2e8f0;
            margin-bottom: 0.45rem;
        }

        .mock-line.short { width: 52%; }
        .mock-line.mid { width: 74%; }
        .mock-line.long { width: 92%; }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_hero(title: str, subtitle: str, chips: Optional[List[str]] = None):
    chip_html = ""
    if chips:
        chip_html = "".join([f'<span class="app-chip">{chip}</span>' for chip in chips])
    st.markdown(
        f"""
        <div class="app-hero">
            <h2 style="margin: 0 0 .2rem 0;">{title}</h2>
            <p style="margin: 0 0 .65rem 0;">{subtitle}</p>
            <div>{chip_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
