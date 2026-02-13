import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-color: #f8fafc;
    }
    [data-testid="stHeader"] {
        background-color: #f8fafc;
    }
    .stButton > button {
        background-color: #1e40af;
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
        box-shadow: 0 0 0 3px rgba(30,64,175,0.25) !important;
    }
    [data-testid="stTextInput"] input {
        border-radius: 8px;
        border: 1.5px solid #cbd5e1 !important;
        font-size: 15px;
        transition: border-color 0.2s;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: #1e40af !important;
        box-shadow: 0 0 0 3px rgba(30,64,175,0.12) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stExpander"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        background: white;
    }
    hr { border-color: #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)


def page_header():
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px;">
            <div style="width:4px;height:40px;background:#1e40af;
                        border-radius:2px;flex-shrink:0;"></div>
            <div>
                <div style="font-size:26px;font-weight:800;color:#0f172a;line-height:1.1;">
                    Generate News Reports
                </div>
                <div style="font-size:13px;color:#64748b;margin-top:4px;">
                    Powered by AI agents
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def tile(icon, label, value):
    return f"""
    <div style="
        background:white;
        border:1px solid #e2e8f0;
        border-radius:12px;
        padding:16px 14px;
        text-align:center;
        min-height:90px;
        box-shadow:0 1px 3px rgba(0,0,0,0.06);
    ">
        <div style="font-size:11px;color:#94a3b8;font-weight:600;
                    text-transform:uppercase;letter-spacing:0.8px;
                    margin-bottom:8px;">{icon} {label}</div>
        <div style="font-size:14px;font-weight:600;color:#1e293b;
                    word-wrap:break-word;line-height:1.5;">{value}</div>
    </div>"""
