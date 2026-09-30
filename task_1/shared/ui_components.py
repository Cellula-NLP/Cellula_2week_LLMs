import html
import streamlit as st

def render_header() -> None:
    st.markdown(
        """<div class="hero-banner"><div class="hero-title">Toxic Content Classifier</div></div>""",
        unsafe_allow_html=True,
    )

def render_result(label: str, score: float, content: str, source: str) -> None:
    """Render a styled result card for the classification output."""
    is_toxic = "toxic" in label.lower() and "non" not in label.lower()
    css_class = "result-toxic" if is_toxic else "result-safe"
    title = "Toxic Content Detected" if is_toxic else "Content is Safe"
    badge_text = "Toxic" if is_toxic else "Safe"

    safe_content = html.escape(content).replace("\n", "<br>")
    safe_title = html.escape(title)

    # SVG Icons (Clean, no emojis)
    icon_svg = """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
        <line x1="12" y1="9" x2="12" y2="13"></line>
        <line x1="12" y1="17" x2="12.01" y2="17"></line>
    </svg>
    """ if is_toxic else """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
    </svg>
    """

    # Use string concatenation to avoid Markdown parsing bugs with newlines
    html_string = (
        f'<div class="result-card {css_class}">'
        f'<div class="result-header">'
        f'<h3 style="display: flex; align-items: center; gap: 10px;">{icon_svg} {safe_title}</h3>'
        f'<span class="badge">{badge_text}</span>'
        f'</div>'
        f'<div class="result-body">'
        f'<p><b>Source:</b> {source}</p>'
        f'<p><b>Content:</b> {safe_content}</p>'
        f'<div class="confidence-container">'
        f'<div class="confidence-fill" style="width: {score * 100}%;"></div>'
        f'</div>'
        f'<div class="confidence-text">'
        f'<span>Confidence Score</span>'
        f'<span>{score * 100:.2f}%</span>'
        f'</div>'
        f'</div>'
        f'</div>'
    )

    st.markdown(html_string, unsafe_allow_html=True)

def render_sidebar(db) -> None:
    """Sidebar with live metrics, database table and clear option."""
    with st.sidebar:
        st.markdown("### Dashboard")
        df = db.get_all_records()
        total = len(df)

        # Strict equality to avoid matching "non-toxic"
        if total > 0:
            toxic_count = len(df[df["Classification"].str.lower().str.strip() == "toxic"])
        else:
            toxic_count = 0

        safe_count = total - toxic_count

        c1, c2, c3 = st.columns(3)
        c1.metric("Total", total)
        c2.metric("Toxic", toxic_count)
        c3.metric("Safe", safe_count)

        st.divider()

        with st.expander("View All Records", expanded=False):
            if df.empty:
                st.info("No records yet.")
            else:
                st.dataframe(df.tail(50), use_container_width=True, hide_index=True)

        st.divider()

        # Confirmation logic for clearing database
        if st.button("Clear Database", use_container_width=True, type="primary"):
            if st.session_state.get("confirm_clear", False):
                db.clear_database()
                st.session_state["confirm_clear"] = False
                st.success("Database cleared.")
                st.rerun()
            else:
                st.session_state["confirm_clear"] = True
                st.warning("Click again to confirm deletion.")