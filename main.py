"""Entry point:  streamlit run main.py"""
import time

import cv2
import streamlit as st

import config
import ui
from database import DatabaseManager
from detector import ObjectDetector


@st.cache_resource
def load_detector():
    return ObjectDetector(config.MODEL_PATH)


@st.cache_resource
def load_database():
    db = DatabaseManager(config.DB_CONFIG)
    db.connect()
    return db


def main():
    ui.setup_page()
    detector = load_detector()
    db = load_database()

    settings = ui.render_sidebar(detector.class_names, config.DEFAULT_CONFIDENCE)
    if db.conn is None:
        st.sidebar.error("MySQL not connected - check your .env file")
    else:
        st.sidebar.success("MySQL connected")

    video_slot, metrics_slot, table_slot = ui.render_layout()
    ui.show_table(table_slot, db.get_recent_logs(config.RECENT_LOGS_LIMIT))

    if not settings["run"]:
        st.info("Turn on **Start detection** in the sidebar.")
        return

    source = int(settings["source"]) if settings["source"].isdigit() else settings["source"]
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        st.error("Could not open the video source.")
        return

    last_logged = {}          # class -> last log time (cooldown)
    session_logged = 0
    last_table_refresh = 0.0
    db_total = db.total_count()
    prev = time.time()
    fps = 0.0

    try:
        while settings["run"]:
            ok, frame = cap.read()
            if not ok:
                st.warning("Video ended or frame could not be read.")
                break

            annotated, detections = detector.detect(
                frame, settings["conf"], settings["classes"] or None
            )

            # Log with a per-class cooldown
            now = time.time()
            if settings["log_to_db"]:
                to_log = []
                for d in detections:
                    if now - last_logged.get(d["object_class"], 0) >= config.LOG_COOLDOWN_SECONDS:
                        to_log.append(d)
                        last_logged[d["object_class"]] = now
                session_logged += db.log_detections(to_log)

            fps = 0.9 * fps + 0.1 * (1.0 / max(now - prev, 1e-6))
            prev = now

            ui.show_frame(video_slot, annotated)
            if now - last_table_refresh > 1.0:   # refresh table + total ~once/sec
                db_total = db.total_count()
                ui.show_table(table_slot, db.get_recent_logs(config.RECENT_LOGS_LIMIT))
                last_table_refresh = now

            ui.show_metrics(metrics_slot, fps, len(detections), session_logged, db_total)
    finally:
        cap.release()


if __name__ == "__main__":
    main()
