import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    /* ── Color tokens ─────────────────────────────────────────────────────── */
    :root {
        --c-bg:         #f8fafc;
        --c-surface:    #ffffff;
        --c-border:     #e2e8f0;
        --c-text:       #0f172a;
        --c-text-sub:   #64748b;
        --c-text-muted: #94a3b8;
        --c-accent:     #1e40af;
        --c-shadow:     rgba(0,0,0,0.06);
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --c-bg:         #0f172a;
            --c-surface:    #1e293b;
            --c-border:     #334155;
            --c-text:       #f1f5f9;
            --c-text-sub:   #94a3b8;
            --c-text-muted: #64748b;
            --c-accent:     #3b82f6;
            --c-shadow:     rgba(0,0,0,0.25);
        }
    }

    /* ── App background ───────────────────────────────────────────────────── */
    [data-testid="stAppViewContainer"] > .main {
        background-color: var(--c-bg);
    }
    [data-testid="stHeader"] {
        background-color: var(--c-bg);
    }

    /* ── Button ───────────────────────────────────────────────────────────── */
    .stButton > button {
        background-color: var(--c-accent);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 15px;
        padding: 0.55rem 1.5rem;
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1d4ed8 !important;
        border: none;
        color: white !important;
    }
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(59,130,246,0.3) !important;
    }

    /* ── Text input ───────────────────────────────────────────────────────── */
    [data-testid="stTextInput"] input {
        border-radius: 8px;
        border: 1.5px solid var(--c-border) !important;
        font-size: 15px;
        transition: border-color 0.2s;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--c-accent) !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    }

    /* ── Sidebar ──────────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: var(--c-surface);
        border-right: 1px solid var(--c-border);
    }

    /* ── Expander — remove hardcoded white background ─────────────────────── */
    [data-testid="stExpander"] {
        border: 1px solid var(--c-border) !important;
        border-radius: 10px !important;
        background: transparent !important;
    }

    hr { border-color: var(--c-border); }

    /* ── Header component ─────────────────────────────────────────────────── */
    .nbg-header { margin-bottom: 1.5rem; }
    .nbg-header-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 4px;
    }
    .nbg-header-bar {
        width: 4px;
        height: 40px;
        background: var(--c-accent);
        border-radius: 2px;
        flex-shrink: 0;
    }
    .nbg-header-title {
        font-size: 26px;
        font-weight: 800;
        color: var(--c-text);
        line-height: 1.1;
    }
    .nbg-header-subtitle {
        font-size: 13px;
        color: var(--c-text-sub);
        margin-top: 4px;
    }

    /* ── Tile component ───────────────────────────────────────────────────── */
    .nbg-tile {
        background: var(--c-surface);
        border: 1px solid var(--c-border);
        border-radius: 12px;
        padding: 16px 14px;
        text-align: center;
        min-height: 90px;
        box-shadow: 0 1px 3px var(--c-shadow);
    }
    .nbg-tile-label {
        font-size: 11px;
        color: var(--c-text-muted);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    .nbg-tile-value {
        font-size: 14px;
        font-weight: 600;
        color: var(--c-text);
        word-wrap: break-word;
        line-height: 1.5;
    }

    /* ── Mobile ───────────────────────────────────────────────────────────── */
    @media (max-width: 640px) {
        [data-testid="stAppViewContainer"] > .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
        }
        .nbg-header-title { font-size: 22px; }
        .stButton > button { font-size: 14px; }
        /* 16px prevents iOS Safari from auto-zooming on input focus */
        [data-testid="stTextInput"] input { font-size: 16px !important; }
    }
    </style>
    """, unsafe_allow_html=True)


def page_header():
    st.markdown("""
    <div class="nbg-header">
        <div class="nbg-header-row">
            <div class="nbg-header-bar"></div>
            <div>
                <div class="nbg-header-title">Generate News Reports</div>
                <div class="nbg-header-subtitle">Powered by AI agents</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def tile(icon, label, value):
    return f"""
    <div class="nbg-tile">
        <div class="nbg-tile-label">{icon} {label}</div>
        <div class="nbg-tile-value">{value}</div>
    </div>"""
