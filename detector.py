"""YOLO detection + drawing of bounding boxes."""
import cv2
from ultralytics import YOLO


class ObjectDetector:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.class_names = list(self.model.names.values())

    def detect(self, frame, conf_threshold=0.7, allowed_classes=None):
        """Run YOLO on a BGR frame.

        Returns (annotated_frame, detections) where each detection is a dict:
        {object_class, confidence, bbox_x, bbox_y, bbox_w, bbox_h}
        """
        result = self.model(frame, conf=conf_threshold, verbose=False)[0]
        annotated = frame.copy()
        detections = []

        for box in result.boxes:
            name = self.model.names[int(box.cls[0])]
            if allowed_classes and name not in allowed_classes:
                continue

            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1

            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{name} {conf:.0%}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(annotated, (x1, y1 - th - 8), (x1 + tw + 4, y1), (0, 255, 0), -1)
            cv2.putText(annotated, label, (x1 + 2, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

            detections.append({
                "object_class": name,
                "confidence": round(conf, 4),
                "bbox_x": x1, "bbox_y": y1, "bbox_w": w, "bbox_h": h,
            })
        return annotated, detections
