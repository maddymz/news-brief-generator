import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    /* ── Import Google Fonts ──────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ── Color tokens ─────────────────────────────────────────────────────── */
    :root {
        --c-bg:         #f8fafc;
        --c-bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --c-surface:    #ffffff;
        --c-border:     #e2e8f0;
        --c-text:       #0f172a;
        --c-text-sub:   #64748b;
        --c-text-muted: #94a3b8;
        --c-accent:     #667eea;
        --c-accent-hover: #5568d3;
        --c-shadow:     rgba(0,0,0,0.06);
        --c-shadow-lg:  rgba(0,0,0,0.12);
        --font-main:    'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --c-bg:         #0f172a;
            --c-bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --c-surface:    #1e293b;
            --c-border:     #334155;
            --c-text:       #f1f5f9;
            --c-text-sub:   #94a3b8;
            --c-text-muted: #64748b;
            --c-accent:     #818cf8;
            --c-accent-hover: #a5b4fc;
            --c-shadow:     rgba(0,0,0,0.25);
            --c-shadow-lg:  rgba(0,0,0,0.5);
        }
    }

    /* ── Global styles ────────────────────────────────────────────────────── */
    * {
        font-family: var(--font-main) !important;
    }

    /* ── App background ───────────────────────────────────────────────────── */
    [data-testid="stAppViewContainer"] > .main {
        background-color: var(--c-bg);
    }
    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 2rem !important;
        max-width: 900px !important;
    }

    /* ── Button ───────────────────────────────────────────────────────────── */
    .stButton > button {
        background: var(--c-bg-gradient);
        color: white !important;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        padding: 0.75rem 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        letter-spacing: 0.3px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
        border: none;
        color: white !important;
    }
    .stButton > button:active {
        transform: translateY(0);
    }
    .stButton > button:focus {
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3), 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }

    /* ── Text input ───────────────────────────────────────────────────────── */
    [data-testid="stTextInput"] input {
        border-radius: 12px;
        border: 2px solid var(--c-border) !important;
        font-size: 15px;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease;
        background: var(--c-surface);
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--c-accent) !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.12) !important;
        transform: translateY(-1px);
    }

    /* ── Sidebar ──────────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: var(--c-surface);
        border-right: 1px solid var(--c-border);
    }

    [data-testid="stSidebar"] h2 {
        font-size: 18px;
        font-weight: 700;
        color: var(--c-text);
    }

    /* ── Expander ─────────────────────────────────────────────────────────── */
    [data-testid="stExpander"] {
        border: 2px solid var(--c-border) !important;
        border-radius: 16px !important;
        background: var(--c-surface) !important;
        overflow: hidden;
        transition: all 0.2s ease;
    }
    [data-testid="stExpander"]:hover {
        border-color: var(--c-accent) !important;
        box-shadow: 0 4px 12px var(--c-shadow-lg);
    }

    [data-testid="stExpander"] summary {
        font-weight: 600;
        font-size: 16px;
        color: var(--c-text);
        padding: 1rem !important;
    }

    /* ── Image styling ────────────────────────────────────────────────────── */
    [data-testid="stImage"] img {
        border-radius: 16px;
        box-shadow: 0 8px 24px var(--c-shadow-lg);
        transition: transform 0.3s ease;
    }
    [data-testid="stImage"] img:hover {
        transform: scale(1.02);
    }

    /* ── Spinner ──────────────────────────────────────────────────────────── */
    .stSpinner > div {
        border-top-color: var(--c-accent) !important;
    }

    hr {
        border-color: var(--c-border);
        margin: 2rem 0;
        opacity: 0.5;
    }

    /* ── Header component ─────────────────────────────────────────────────── */
    .nbg-header {
        margin-bottom: 2.5rem;
        position: relative;
    }
    .nbg-header-row {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 8px;
        padding: 1.5rem;
        background: var(--c-bg-gradient);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    .nbg-header-icon {
        font-size: 48px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    .nbg-header-content {
        flex: 1;
    }
    .nbg-header-title {
        font-size: 32px;
        font-weight: 800;
        color: white;
        line-height: 1.2;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .nbg-header-subtitle {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
        letter-spacing: 0.3px;
    }

    /* ── Tile component ───────────────────────────────────────────────────── */
    .nbg-tile {
        background: var(--c-surface);
        border: 2px solid var(--c-border);
        border-radius: 16px;
        padding: 20px 18px;
        text-align: center;
        min-height: 110px;
        box-shadow: 0 2px 8px var(--c-shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .nbg-tile::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--c-bg-gradient);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .nbg-tile:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px var(--c-shadow-lg);
        border-color: var(--c-accent);
    }
    .nbg-tile:hover::before {
        opacity: 1;
    }
    .nbg-tile-icon {
        font-size: 28px;
        margin-bottom: 8px;
        display: block;
    }
    .nbg-tile-label {
        font-size: 11px;
        color: var(--c-text-muted);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .nbg-tile-value {
        font-size: 15px;
        font-weight: 600;
        color: var(--c-text);
        word-wrap: break-word;
        line-height: 1.5;
    }

    /* ── Article section ──────────────────────────────────────────────────── */
    .nbg-article-container {
        background: var(--c-surface);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid var(--c-border);
        box-shadow: 0 4px 16px var(--c-shadow);
    }

    /* ── Loading animation ────────────────────────────────────────────────── */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .nbg-tile, .nbg-header-row {
        animation: fadeIn 0.5s ease-out;
    }

    /* ── Mobile ───────────────────────────────────────────────────────────── */
    @media (max-width: 640px) {
        [data-testid="stAppViewContainer"] > .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
        }
        .nbg-header-title { font-size: 24px; }
        .nbg-header-subtitle { font-size: 12px; }
        .nbg-header-icon { font-size: 36px; }
        .nbg-header-row { padding: 1rem; }
        .stButton > button {
            font-size: 14px;
            padding: 0.65rem 1.5rem;
        }
        .nbg-tile {
            min-height: 100px;
            padding: 16px 14px;
        }
        /* 16px prevents iOS Safari from auto-zooming on input focus */
        [data-testid="stTextInput"] input { font-size: 16px !important; }
    }
    </style>
    """, unsafe_allow_html=True)


def page_header():
    st.markdown("""
    <div class="nbg-header">
        <div class="nbg-header-row">
            <div class="nbg-header-icon">📰</div>
            <div class="nbg-header-content">
                <div class="nbg-header-title">News Brief Generator</div>
                <div class="nbg-header-subtitle">AI-powered contextual news reports with live data</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def tile(icon, label, value):
    return f"""
    <div class="nbg-tile">
        <div class="nbg-tile-icon">{icon}</div>
        <div class="nbg-tile-label">{label}</div>
        <div class="nbg-tile-value">{value}</div>
    </div>"""
