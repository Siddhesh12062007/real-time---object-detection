"""Streamlit UI components (no detection or DB logic here)."""
import pandas as pd
import streamlit as st


def setup_page():
    st.set_page_config(page_title="Real-Time Object Detection", page_icon="🎥", layout="wide")
    st.title("🎥 Real-Time Object Detection Platform")
    st.caption("YOLO + OpenCV + MySQL event logging")


def render_sidebar(class_names: list, default_conf: float) -> dict:
    st.sidebar.header("⚙️ Settings")
    source = st.sidebar.text_input("Video source (0 = webcam, or file path)", "0")
    conf = st.sidebar.slider("Confidence threshold", 0.10, 0.95, default_conf, 0.05)
    classes = st.sidebar.multiselect(
        "Classes to detect (empty = all)", class_names, default=["person"]
    )
    log_to_db = st.sidebar.checkbox("Log events to MySQL", value=True)
    run = st.sidebar.toggle("▶ Start detection", value=False)
    return {"source": source, "conf": conf, "classes": classes,
            "log_to_db": log_to_db, "run": run}


def render_layout():
    """Returns placeholders: video, metrics row, table."""
    left, right = st.columns([3, 2])
    with left:
        st.subheader("Live Feed")
        video_slot = st.empty()
    with right:
        st.subheader("Metrics")
        metrics_slot = st.empty()
        st.subheader("Recent Database Logs")
        table_slot = st.empty()
    return video_slot, metrics_slot, table_slot


def show_frame(slot, frame_bgr):
    slot.image(frame_bgr, channels="BGR", use_container_width=True)


def show_metrics(slot, fps: float, current: int, session_logged: int, db_total: int):
    with slot.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("FPS", f"{fps:.1f}")
        c2.metric("Objects now", current)
        c3.metric("Logged (session)", session_logged)
        c4.metric("DB total", db_total)


def show_table(slot, rows: list):
    if rows:
        slot.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        slot.info("No logs yet (or database not connected).")
