# Real-Time Object Detection Platform

A modular real-time object detection platform built with **Python, OpenCV and YOLOv8**, with **MySQL** event logging and a **Streamlit** dashboard.

## Features
- Live webcam / video-file detection with bounding boxes
- Filter by object class (e.g. only `person`, `cell phone`)
- Adjustable confidence threshold (default 70%)
- Detection events saved to MySQL in real time (per-class cooldown avoids flooding)
- Dashboard: live annotated feed, FPS / object metrics, table of latest DB logs
- No hardcoded credentials (`.env`)

## Project Structure
| File | Purpose |
|---|---|
| `main.py` | App entry point, ties everything together |
| `detector.py` | YOLO inference + drawing boxes |
| `database.py` | MySQL connection, inserts, queries |
| `ui.py` | Streamlit dashboard components |
| `config.py` | Settings loaded from `.env` |
| `database_schema.sql` | Creates `vision_platform` DB and `detection_logs` table |

## Setup
1. Install Python 3.10+ and start MySQL (XAMPP / WAMP / MySQL Workbench).
2. Create the database:
   ```bash
   mysql -u root -p < database_schema.sql
   ```
3. Install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows  (Linux/Mac: source venv/bin/activate)
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and set your MySQL credentials.
5. Run:
   ```bash
   streamlit run main.py
   ```
6. In the sidebar choose classes / confidence and switch on **Start detection**.

## Verify logging
```sql
USE vision_platform;
SELECT * FROM detection_logs ORDER BY log_id DESC LIMIT 10;
```

## Database Schema
`log_id` (PK), `timestamp`, `object_class`, `confidence`, `bbox_x`, `bbox_y`, `bbox_w`, `bbox_h`

## Demo
- Video: _add link_
- Medium article: _add link_
