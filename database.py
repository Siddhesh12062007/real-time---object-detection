"""MySQL event logging."""
import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    def __init__(self, db_config: dict):
        self.config = db_config
        self.conn = None

    def connect(self) -> bool:
        try:
            self.conn = mysql.connector.connect(**self.config)
            return True
        except Error as e:
            print(f"[DB] Connection failed: {e}")
            self.conn = None
            return False

    def _ensure_connection(self) -> bool:
        if self.conn is None:
            return self.connect()
        try:
            self.conn.ping(reconnect=True, attempts=2, delay=1)
            return True
        except Error:
            return self.connect()

    def log_detections(self, detections: list) -> int:
        """Insert a list of detection dicts. Returns number of rows saved."""
        if not detections or not self._ensure_connection():
            return 0
        sql = (
            "INSERT INTO detection_logs "
            "(object_class, confidence, bbox_x, bbox_y, bbox_w, bbox_h) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        rows = [(d["object_class"], d["confidence"], d["bbox_x"],
                 d["bbox_y"], d["bbox_w"], d["bbox_h"]) for d in detections]
        try:
            cur = self.conn.cursor()
            cur.executemany(sql, rows)
            self.conn.commit()
            cur.close()
            return len(rows)
        except Error as e:
            print(f"[DB] Insert failed: {e}")
            return 0

    def get_recent_logs(self, limit: int = 15) -> list:
        if not self._ensure_connection():
            return []
        try:
            cur = self.conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM detection_logs ORDER BY log_id DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
            cur.close()
            return rows
        except Error as e:
            print(f"[DB] Query failed: {e}")
            return []

    def total_count(self) -> int:
        if not self._ensure_connection():
            return 0
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM detection_logs")
            n = cur.fetchone()[0]
            cur.close()
            return n
        except Error:
            return 0

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
