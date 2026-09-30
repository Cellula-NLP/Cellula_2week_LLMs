import streamlit as st
from .config import *


def inject_custom_css() -> None:
    st.markdown(
        f"""
        <style>
        /* Import modern font */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', sans-serif; }}

        /* ---- Global App Styling ---- */
        .stApp {{ 
            background: {BG_GRADIENT} !important;
            color: {TEXT_MAIN} !important;
        }}
        h1, h2, h3, h4, h5, h6, p, span, div, label {{ 
            color: {TEXT_MAIN} !important; 
        }}

        /* ---- header ---- */
        [data-testid="stHeader"] {{
            background: transparent !important;
            border-bottom: none !important;
        }}

        #MainMenu, footer, .stDeployButton {{ 
            visibility: hidden; 
            display: none;
        }}

        /* ---- Animated Header Banner ---- */
        .hero-banner {{
            background: linear-gradient(-45deg, #0F766E, #14B8A6, #0D9488, #115E59) !important;
            background-size: 400% 400% !important;
            animation: gradientMove 8s ease infinite !important;
            border: 1px solid {CARD_BORDER};
            padding: 3rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}
        .hero-title {{
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        @keyframes gradientMove {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* ---- Sidebar Styling ---- */
        section[data-testid="stSidebar"] {{
            background-color: #0B3B36 !important;
            border-right: 1px solid {CARD_BORDER};
        }}
        section[data-testid="stSidebar"] * {{
            color: {TEXT_MAIN} !important;
        }}

        .streamlit-expanderHeader {{
            background-color: {CARD_BG} !important;
            border-radius: 8px !important;
            border: 1px solid {CARD_BORDER} !important;
        }}
        .streamlit-expanderHeader svg {{ fill: {TEXT_MAIN} !important; }}
        .streamlit-expanderContent {{
            background-color: rgba(0, 0, 0, 0.2) !important;
            border: 1px solid {CARD_BORDER} !important;
            border-top: none !important;
            border-radius: 0 0 8px 8px !important;
        }}

        [data-testid="stDataFrame"] {{
            background-color: {CARD_BG} !important;
            border-radius: 8px;
            border: 1px solid {CARD_BORDER};
        }}
        [data-testid="stDataFrame"] div {{ color: {TEXT_MAIN} !important; }}

        /* ---- Trendy Tabs ---- */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: rgba(0, 0, 0, 0.25);
            padding: 6px;
            border-radius: 16px;
            width: fit-content;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.3);
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 45px;
            background-color: transparent;
            border-radius: 12px;
            padding: 0 28px;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.5) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: none !important;
            position: relative;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            color: {TEXT_MAIN} !important;
            background-color: rgba(255, 255, 255, 0.05);
        }}
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {TEAL_ACCENT} 0%, {TEAL_HOVER} 100%) !important;
            box-shadow: 0 6px 20px rgba(20, 184, 166, 0.4) !important;
            transform: translateY(-2px);
        }}
        .stTabs [aria-selected="true"] p {{
            color: {TEXT_MAIN} !important;
            font-weight: 700 !important;
        }}
        .stTabs [aria-selected="true"]::after {{
            content: '';
            position: absolute;
            bottom: -4px;
            left: 20%;
            width: 60%;
            height: 2px;
            background: #5EEAD4;
            border-radius: 2px;
            box-shadow: 0 0 8px #5EEAD4;
        }}

        /* ---- Buttons ---- */
        .stButton > button {{
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: {TEXT_MAIN} !important;
            border: 1px solid {CARD_BORDER} !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            width: 100%;
            backdrop-filter: blur(5px);
        }}
        .stButton > button:hover {{
            background-color: rgba(255, 255, 255, 0.2) !important;
            transform: translateY(-2px);
        }}
        .stButton > button[kind="primary"] {{
            background-color: {TEAL_ACCENT} !important;
            color: {TEXT_MAIN} !important;
            border: none !important;
            box-shadow: 0 4px 6px rgba(20, 184, 166, 0.3);
        }}
        .stButton > button[kind="primary"]:hover {{
            background-color: {TEAL_HOVER} !important;
            box-shadow: 0 10px 15px rgba(20, 184, 166, 0.4);
        }}
        .stButton > button p {{ color: inherit !important; margin: 0 !important; }}

        /* ---- File Uploader ---- */
        [data-testid="stFileUploadDropzone"] {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 2px dashed rgba(255, 255, 255, 0.3) !important;
            border-radius: 14px !important;
            transition: all 0.3s ease;
        }}
        [data-testid="stFileUploadDropzone"]:hover {{
            border-color: {TEAL_ACCENT} !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
        }}
        [data-testid="stFileUploadDropzone"] * {{ color: {TEXT_MAIN} !important; }}
        [data-testid="stFileUploadDropzone"] button {{
            background-color: {TEAL_ACCENT} !important;
            color: {TEXT_MAIN} !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }}
        [data-testid="stFileUploadDropzone"] button:hover {{
            background-color: {TEAL_HOVER} !important;
            transform: scale(1.05);
        }}
        [data-testid="stFileUploadDropzone"] button * {{ color: {TEXT_MAIN} !important; }}

        /* ---- Text Area ---- */
        .stTextArea textarea {{
            border-radius: 14px !important;
            border: 2px solid {CARD_BORDER} !important;
            padding: 1.2rem !important;
            font-size: 1rem !important;
            background-color: rgba(0, 0, 0, 0.2) !important;
            color: {TEXT_MAIN} !important;
            transition: all 0.3s ease;
        }}
        .stTextArea textarea::placeholder {{ color: rgba(255, 255, 255, 0.5) !important; }}
        .stTextArea textarea:focus {{
            border-color: {TEAL_ACCENT} !important;
            box-shadow: 0 0 0 4px rgba(20, 184, 166, 0.2) !important;
            background-color: rgba(0, 0, 0, 0.3) !important;
        }}

        /* ---- Result Cards ---- */
        .result-card {{
            padding: 1.8rem;
            border-radius: 16px;
            margin: 2rem 0;
            background: {CARD_BG};
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid {CARD_BORDER};
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
            animation: slideUp 0.4s ease-out forwards;
        }}
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .result-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }}
        .result-header h3 {{ margin: 0; font-size: 1.4rem; }}
        .badge {{
            padding: 0.4rem 1rem;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .result-toxic .badge {{ background-color: rgba(239, 68, 68, 0.2); color: {TOXIC_COLOR}; }}
        .result-safe .badge {{ background-color: rgba(16, 185, 129, 0.2); color: {SAFE_COLOR}; }}
        .result-toxic {{ border-left: 6px solid {TOXIC_COLOR}; }}
        .result-safe  {{ border-left: 6px solid {SAFE_COLOR}; }}

        .result-body p {{ margin-bottom: 1rem; color: {TEXT_MUTED} !important; line-height: 1.6; }}
        .result-body p b {{ color: {TEXT_MAIN}; }}

        .confidence-container {{
            margin-top: 1.5rem;
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 50px;
            height: 10px;
            overflow: hidden;
        }}
        .confidence-fill {{
            height: 100%;
            border-radius: 50px;
            transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .result-toxic .confidence-fill {{ background: linear-gradient(90deg, #F87171, {TOXIC_COLOR}); }}
        .result-safe .confidence-fill {{ background: linear-gradient(90deg, #34D399, {SAFE_COLOR}); }}
        .confidence-text {{
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: {TEXT_MUTED};
            margin-top: 0.5rem;
            font-weight: 500;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )