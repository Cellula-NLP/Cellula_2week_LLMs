"""
Architecture:
    - Streamlit UI  ->  app.py
    - Image Captioning  ->  imagecaption.py (BLIP)
    - Text Classification  ->  textclassifier.py (DistilBERT based model)
    - Persistence  ->  database.py (CSV)
    - Styling  ->  styles.py
    - UI Components  ->  ui_components.py
    - Utils  ->  utils.py
    - Config  ->  config.py
"""

import streamlit as st
from PIL import Image

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Toxic Content Classifier",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import custom modules
from shared.styles import inject_custom_css
from shared.ui_components import render_header, render_result, render_sidebar
from shared.utils import is_online, validate_image

# 2. MODEL LOADING (High Performance Caching)
@st.cache_resource(show_spinner=False)
def load_pipeline():
    """Load both AI models once and reuse them across reruns."""
    from imagecaption import ImageCaptioner
    from textclassifier import ToxicityClassifier

    captioner = ImageCaptioner()
    classifier = ToxicityClassifier()
    return captioner, classifier

# 3. MAIN APP
def main() -> None:
    # Setup UI
    inject_custom_css()
    render_header()

    # Check internet connectivity
    if not is_online():
        st.error("**No internet connection detected.** Please reconnect and refresh.")
        st.stop()

    # Initialize Database
    from database import DatabaseManager
    db = DatabaseManager()

    # Load Models
    with st.spinner("🔧 Loading AI models... (Just moment :) )"):
        try:
            captioner, classifier = load_pipeline()
        except Exception as exc:
            st.error(f"Failed to load AI models: {exc}")
            st.info("Please verify your internet connection and restart the app.")
            st.stop()

    # --- Tabs ---
    tab_text, tab_image = st.tabs(["Text Input", "Image Input"])

    # ---------- Tab 1: Text ----------
    with tab_text:
        st.subheader("Classify Text")
        user_text = st.text_area(
            "Enter the text you want to check:",
            placeholder="Type or paste text here...",
            height=150,
            max_chars=5000,
            key="text_input",
        )

        def clear_text_callback():
            st.session_state["text_input"] = ""

        c1, c2 = st.columns([1, 4])
        with c1:
            submit_text = st.button("Classify Text", use_container_width=True, type="primary", key="btn_text")
        with c2:
            st.button("Clear", key="clear_text", on_click=clear_text_callback, use_container_width=True, type="secondary")

        if submit_text:
            if not user_text.strip():
                st.warning("Please enter some text before submitting.")
            else:
                with st.spinner("Analyzing..."):
                    result = classifier.classify(user_text)
                    render_result(result["label"], result["score"], user_text, "Text Input")
                    db.save_record("Text", user_text, result["label"])
                    st.success("Record saved to database.")

    # ---------- Tab 2: Image ----------
    with tab_image:
        st.subheader("Classify Image Caption")
        uploaded_file = st.file_uploader(
            "Upload an image (JPG / JPEG / PNG, max 5 MB):",
            type=["jpg", "jpeg", "png"],
            key="image_uploader",
        )

        if uploaded_file is not None:
            is_valid, message, image = validate_image(uploaded_file)

            if not is_valid:
                st.error(f"{message}")
            else:
                left, right = st.columns(2)
                with left:
                    st.image(image, caption="Uploaded Image", use_container_width=True)

                with right:
                    if st.button("Generate Caption & Classify", use_container_width=True, type="primary", key="btn_image"):
                        with st.spinner("Generating caption and analyzing..."):
                            caption = captioner.generate_caption(image)
                            st.markdown(f"**Generated Caption:**\n\n> {caption}")

                            result = classifier.classify(caption)
                            render_result(result["label"], result["score"], caption, "Image Caption")
                            db.save_record("Image Caption", caption, result["label"])
                            st.success("Record saved to database.")

    # Render sidebar to ensure metrics update immediately
    render_sidebar(db)

# 4. ENTRY POINT
if __name__ == "__main__":
    main()