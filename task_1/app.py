"""
Toxic Content Classification App
---------------------------------
A production-ready Streamlit application that classifies user-provided
text or image captions as toxic or non-toxic.

Architecture:
    - Streamlit UI  ->  app.py
    - Image Captioning  ->  imagecaption.py (BLIP)
    - Text Classification  ->  textclassifier.py (DistilBERT with LoRA)
    - Persistence  ->  database.py (CSV)
"""

import socket
from io import BytesIO

import pandas as pd
import streamlit as st
from PIL import Image

# 1. PAGE CONFIGURATION (must be the first Streamlit call)
st.set_page_config(
    page_title="Toxic Content Classifier",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. CONSTANTS - Modern, High-Contrast Color Palette
TEAL_PRIMARY = "#0F766E"   # Deep, professional teal
TEAL_LIGHT = "#14B8A6"     # Lighter teal for hover/gradients
BG_MAIN = "#F8FAFC"        # Clean slate background
BG_CARD = "#FFFFFF"        # Pure white cards
TEXT_MAIN = "#1E293B"      # Dark slate for primary text
TEXT_MUTED = "#64748B"     # Muted slate for secondary text
BORDER_COLOR = "#E2E8F0"   # Light border
MAX_CHARS = 200            # Maximum characters for text input
MAX_IMAGE_SIZE_MB = 5
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]


# 3. THEME - Clean, Trendy, High-Contrast CSS
def inject_custom_css() -> None:
    st.markdown(
        f"""
        <style>
        /* Import modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

        /* ---- Global App Styling ---- */
        .stApp {{ background-color: {BG_MAIN}; }}
        h1, h2, h3, h4, h5, h6 {{ color: {TEXT_MAIN} !important; font-weight: 700; letter-spacing: -0.02em; }}
        p, span, div {{ color: {TEXT_MAIN}; }}
        #MainMenu, footer {{ visibility: hidden; }}

        /* ---- Header Banner ---- */
        .app-header {{
            background: linear-gradient(135deg, {TEAL_PRIMARY} 0%, {TEAL_LIGHT} 100%);
            padding: 2.5rem 3rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 15px -3px rgba(15, 118, 110, 0.2), 0 4px 6px -2px rgba(15, 118, 110, 0.1);
        }}
        .app-header h1, .app-header p {{ color: white !important; margin: 0; }}
        .app-header h1 {{ font-size: 2.2rem; font-weight: 700; }}
        .app-header p {{ margin-top: 0.5rem; font-size: 1.1rem; opacity: 0.95; font-weight: 400; }}

        /* ---- Sidebar Styling ---- */
        section[data-testid="stSidebar"] {{
            background-color: {BG_CARD};
            border-right: 1px solid {BORDER_COLOR};
        }}
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{ color: {TEXT_MAIN} !important; }}
        
        /* Sidebar Metrics */
        section[data-testid="stSidebar"] [data-testid="stMetricValue"] {{ color: {TEAL_PRIMARY} !important; font-weight: 700; }}
        section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {{ color: {TEXT_MUTED} !important; font-size: 0.9rem; font-weight: 500; }}

        /* Fix Expander (View All Records) in Sidebar */
        .streamlit-expanderHeader {{
            background-color: #F1F5F9 !important;
            color: {TEXT_MAIN} !important;
            border-radius: 8px !important;
            border: 1px solid {BORDER_COLOR} !important;
        }}
        .streamlit-expanderContent {{
            background-color: {BG_CARD} !important;
            border: 1px solid {BORDER_COLOR} !important;
            border-top: none !important;
            border-radius: 0 0 8px 8px !important;
        }}

        /* ---- Modern Tabs (Segmented Control Design) ---- */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: #F1F5F9;
            padding: 6px;
            border-radius: 12px;
            width: fit-content;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 45px;
            background-color: transparent;
            border-radius: 8px;
            padding: 0 24px;
            font-weight: 600;
            color: {TEXT_MUTED} !important;
            transition: all 0.2s ease;
            border: none !important;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            background-color: #E2E8F0;
            color: {TEAL_PRIMARY} !important;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {BG_CARD} !important;
            color: {TEAL_PRIMARY} !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }}

        /* ---- Buttons (Primary & Secondary) ---- */
        /* Primary Button - Force White Text */
        .stButton > button[kind="primary"], .stButton > button:not([kind="secondary"]) {{
            background-color: {TEAL_PRIMARY} !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 6px -1px rgba(15, 118, 110, 0.2) !important;
            width: 100%;
        }}
        .stButton > button[kind="primary"] p, .stButton > button:not([kind="secondary"]) p {{
            color: #FFFFFF !important; /* Force text inside button to be white */
        }}
        .stButton > button[kind="primary"]:hover, .stButton > button:not([kind="secondary"]):hover {{
            background-color: {TEAL_LIGHT} !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 15px -3px rgba(15, 118, 110, 0.4) !important;
            color: #FFFFFF !important;
        }}
        
        /* Secondary Button (Clear Button) */
        .stButton > button[kind="secondary"] {{
            background-color: #F1F5F9 !important;
            color: {TEXT_MAIN} !important;
            border: 1px solid {BORDER_COLOR} !important;
            border-radius: 10px !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }}
        .stButton > button[kind="secondary"]:hover {{
            background-color: #E2E8F0 !important;
            color: {TEAL_PRIMARY} !important;
            border-color: {TEAL_PRIMARY} !important;
        }}

        /* ---- Text Input & Text Area ---- */
        .stTextInput input, .stTextArea textarea {{
            border-radius: 10px !important;
            border: 2px solid {BORDER_COLOR} !important;
            padding: 0.8rem 1rem !important;
            font-size: 1rem !important;
            background-color: {BG_CARD} !important;
            color: {TEXT_MAIN} !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }}
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{ color: #94A3B8 !important; }}
        .stTextInput input:focus, .stTextArea textarea:focus {{
            border-color: {TEAL_PRIMARY} !important;
            box-shadow: 0 0 0 4px rgba(15, 118, 110, 0.1) !important;
        }}

        /* ---- Result Cards ---- */
        .result-card {{
            padding: 1.5rem 1.8rem;
            border-radius: 12px;
            margin: 1.5rem 0;
            background: {BG_CARD};
            border-left: 6px solid {TEAL_PRIMARY};
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        }}
        .result-toxic {{ border-left-color: #EF4444; background: #FEF2F2; }}
        .result-safe  {{ border-left-color: #10B981; background: #ECFDF5; }}
        .result-toxic h3 {{ color: #991B1B !important; }}
        .result-safe h3 {{ color: #065F46 !important; }}
        .result-card h3 {{ margin-top: 0; font-size: 1.3rem; }}
        .result-card p {{ margin-bottom: 0.5rem; color: #334155 !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# 4. UTILITIES
def is_online(host: str = "huggingface.co", port: int = 443, timeout: int = 3) -> bool:
    """Detect if the machine has internet (needed on first model download)."""
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except OSError:
        return False


def validate_image(uploaded_file) -> tuple[bool, str, Image.Image | None]:
    """Validate an uploaded image file."""
    if uploaded_file is None:
        return False, "No file uploaded.", None

    extension = uploaded_file.name.split(".")[-1].lower()
    if extension not in ALLOWED_IMAGE_TYPES:
        return False, f"Invalid file type '.{extension}'. Allowed: {', '.join(ALLOWED_IMAGE_TYPES)}.", None

    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        return False, f"File too large ({size_mb:.1f} MB). Max allowed: {MAX_IMAGE_SIZE_MB} MB.", None

    try:
        image = Image.open(BytesIO(uploaded_file.getvalue())).convert("RGB")
        return True, "OK", image
    except Exception as exc:
        return False, f"Corrupted or unreadable image: {exc}", None


# 5. MODEL LOADING (High Performance Caching)
@st.cache_resource(show_spinner=False)
def load_pipeline():
    """Load both AI models once and reuse them across reruns."""
    from image_caption import ImageCaptioner
    from text_classifier import ToxicityClassifier

    captioner = ImageCaptioner()
    classifier = ToxicityClassifier()
    return captioner, classifier


# 6. UI COMPONENTS
def render_header() -> None:
    st.markdown(
        """
        <div class="app-header">
            <h1>🔒 Toxic Content Classifier</h1>
            <p>Detect toxic content in user input and images using AI-powered models.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result(label: str, score: float, content: str, source: str) -> None:
    """Render a styled result card for the classification output."""
    is_toxic = "toxic" in label.lower() and "non" not in label.lower()
    css_class = "result-toxic" if is_toxic else "result-safe"
    icon = "⚠️" if is_toxic else "✅"
    title = "Toxic Content Detected" if is_toxic else "Content is Safe"

    st.markdown(
        f"""
        <div class="result-card {css_class}">
            <h3>{icon} {title}</h3>
            <p><b>Source:</b> {source}</p>
            <p><b>Content:</b> {content}</p>
            <p><b>Confidence:</b> {score * 100:.2f}%</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(db) -> None:
    """Sidebar with live metrics, database table and clear option."""
    with st.sidebar:
        st.markdown("### 📊 Analytics Dashboard")
        df = db.get_all_records()
        total = len(df)
        toxic = (
            len(df[df["Classification"].str.lower().str.contains("toxic", na=False)])
            if total > 0
            else 0
        )
        safe = total - toxic

        c1, c2, c3 = st.columns(3)
        c1.metric("Total", total)
        c2.metric("Toxic", toxic)
        c3.metric("Safe", safe)

        st.divider()

        with st.expander("📋 View All Records", expanded=False):
            if df.empty:
                st.info("No records yet.")
            else:
                st.dataframe(df.tail(50), use_container_width=True, hide_index=True)

        st.divider()

        # Confirmation logic for clearing database
        if st.button("🗑️ Clear Database", use_container_width=True, type="primary"):
            if st.session_state.get("confirm_clear", False):
                db.clear_database()
                st.session_state["confirm_clear"] = False
                st.success("Database cleared.")
                st.rerun()
            else:
                st.session_state["confirm_clear"] = True
                st.warning("⚠️ Click again to confirm deletion.")


# 7. MAIN APP
def main() -> None:
    inject_custom_css()
    render_header()

    if not is_online():
        st.error("🚫 **No internet connection detected.** Please reconnect and refresh.")
        st.stop()

    from database import DatabaseManager
    db = DatabaseManager()

    with st.spinner("🔧 Loading AI models... (first run may take a moment)"):
        try:
            captioner, classifier = load_pipeline()
        except Exception as exc:
            st.error(f"❌ Failed to load AI models: {exc}")
            st.info("Please verify your internet connection and restart the app.")
            st.stop()

    render_sidebar(db)

    # --- Modern Tabs ---
    tab_text, tab_image = st.tabs(["📝 Text Input", "🖼️ Image Input"])

    # ---------- Tab 1: Text ----------
    with tab_text:
        st.subheader("Classify Text")
        st.caption(f"Enter up to {MAX_CHARS} characters. Press **Enter** to classify.")

        # Using st.text_input instead of st.text_area to allow "Enter" to submit natively
        user_text = st.text_input(
            "Enter the text you want to check:",
            placeholder="Type or paste text here...",
            max_chars=MAX_CHARS,
            key="text_input",
        )

        # Callback to safely clear the text area
        def clear_text_callback():
            st.session_state["text_input"] = ""

        c1, c2 = st.columns([1, 4])
        with c1:
            submit_text = st.button("🔍 Classify Text", use_container_width=True, type="primary", key="btn_text")
        with c2:
            st.button("Clear", key="clear_text", on_click=clear_text_callback, use_container_width=True, type="secondary")

        if submit_text:
            if not user_text.strip():
                st.warning("⚠️ Please enter some text before submitting.")
            else:
                with st.spinner("Analyzing..."):
                    result = classifier.classify(user_text)
                    render_result(result["label"], result["score"], user_text, "Text Input")
                    db.save_record("Text", user_text, result["label"])
                    st.success("✅ Record saved to database.")

    # ---------- Tab 2: Image ----------
    with tab_image:
        st.subheader("Classify Image Caption")
        uploaded_file = st.file_uploader(
            "Upload an image (JPG / JPEG / PNG, max 5 MB):",
            type=ALLOWED_IMAGE_TYPES,
            key="image_uploader",
        )

        if uploaded_file is not None:
            is_valid, message, image = validate_image(uploaded_file)

            if not is_valid:
                st.error(f"❌ {message}")
            else:
                left, right = st.columns(2)
                with left:
                    st.image(image, caption="Uploaded Image", use_container_width=True)

                with right:
                    with st.spinner("Generating caption..."):
                        caption = captioner.generate_caption(image)
                        st.markdown(f"**Generated Caption:**\n\n> {caption}")

                    if st.button("🔍 Classify Caption", use_container_width=True, type="primary", key="btn_image"):
                        with st.spinner("Analyzing caption..."):
                            result = classifier.classify(caption)
                            render_result(result["label"], result["score"], caption, "Image Caption")
                            db.save_record("Image Caption", caption, result["label"])
                            st.success("✅ Record saved to database.")


# 8. ENTRY POINT
if __name__ == "__main__":
    main()