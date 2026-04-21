from pathlib import Path
from typing import Any

import cv2
import numpy as np
from ultralytics import YOLO


class ClothingDetector:
    """
        Clothing detector using a fine-tuned YOLO11 model.
        """

    LABEL_MAPPING = {
        "shirt": {"label": "shirt", "category": "top"},
        "long shirt": {"label": "long shirt", "category": "top"},
        "sleevelessshirt": {"label": "sleeveless shirt", "category": "top"},
        "hoodie": {"label": "hoodie", "category": "top"},
        "jacket": {"label": "jacket", "category": "top"},
        "long pants": {"label": "long pants", "category": "bottom"},
        "short": {"label": "shorts", "category": "bottom"},
        "long skirt": {"label": "dress", "category": "dress"},
        "short skirt": {"label": "short skirt", "category": "bottom"},
        "sport shoes": {"label": "shoes", "category": "footwear"},
        "flats": {"label": "flats", "category": "footwear"},
        "high heel": {"label": "high heels", "category": "footwear"},
        "slipper": {"label": "slipper", "category": "footwear"},
    }

    IGNORED_LABELS = {"male", "female", "exposed"}

    def __init__(self, model_name: str = "src/ai/models/best.pt") -> None:
        self.model = YOLO(model_name)

    def normalize_label(self, label: str) -> str | None:
        raw = label.lower().strip()

        if raw in self.IGNORED_LABELS:
            return None

        return self.LABEL_MAPPING.get(
            raw,
            {"label": raw, "category": "unknown"}
        )

    def detect(self, image_path: str | Path, conf: float = 0.25) -> list[dict[str, Any]]:
        print(f"Running detection on: {image_path}")
        print(f"Confidence threshold: {conf}")

        results = self.model.predict(
            source=str(image_path),
            conf=conf,
            verbose=False
        )

        detections: list[dict[str, Any]] = []

        if not results:
            return detections

        result = results[0]


        if result.boxes is None or len(result.boxes) == 0:
            return detections


        print("Result names:", result.names)
        print("Number of boxes:", len(result.boxes))

        for box in result.boxes:
            cls_id = int(box.cls[0].item())
            confidence = float(box.conf[0].item())
            coords = box.xyxy[0].tolist()

            raw_label = result.names[cls_id]


            normalized = self.normalize_label(raw_label)

            print(f"Raw label: {raw_label} -> Normalized: {normalized}")

            if normalized is None:
                continue
            detection = {
                "label": normalized["label"],
                "category": normalized["category"],
                "confidence": confidence,
                "bbox": coords
            }

            print("Detection found:", detection)
            detections.append(detection)
        return detections

    def detect_best(self, image_path: str | Path, conf: float = 0.25) -> dict[str, Any] | None:
        detections = self.detect(image_path=image_path, conf=conf)
        if not detections:
            print("No detections found.")
            return None


        best = max(detections, key=lambda d: d["confidence"])
        print("Best detection:", best)
        return best


    def detect_color(self, image_path: str | Path,  bbox: list[float] | None = None) -> str:
        image = cv2.imread(str(image_path))

        if image is None:
            return "unknown"

        h, w, _ = image.shape

        # Default crop: center area of image
        cropped = image[int(h * 0.25):int(h * 0.80), int(w * 0.25):int(w * 0.75)]



        if bbox:
            x1, y1, x2, y2 = map(int, bbox)

            # shrink inward a bit to reduce background noise
            pad_x = int((x2 - x1) * 0.15)
            pad_y = int((y2 - y1) * 0.15)

            x1 += pad_x
            x2 -= pad_x
            y1 += pad_y
            y2 -= pad_y

            # keep bbox inside image bounds
            x1 = max(0, min(x1, w - 1))
            x2 = max(0, min(x2, w))
            y1 = max(0, min(y1, h - 1))
            y2 = max(0, min(y2, h))

            if x2 > x1 and y2 > y1:
                cropped = image[y1:y2, x1:x2]

        if cropped.size == 0:
            return "unknown"

        hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

        color_ranges = {
            "red": [
                ((0, 70, 50), (10, 255, 255)),
                ((170, 70, 50), (180, 255, 255)),
            ],
            "orange": [((11, 70, 50), (25, 255, 255))],
            "yellow": [((26, 70, 50), (35, 255, 255))],
            "green": [((36, 50, 50), (85, 255, 255))],
            "blue": [((86, 50, 50), (130, 255, 255))],
            "purple": [((131, 50, 50), (160, 255, 255))],
            "white": [((0, 0, 200), (180, 35, 255))],
            "gray": [((0, 0, 80), (180, 35, 199))],
            "black": [((0, 0, 0), (180, 255, 79))],
            "brown": [((10, 100, 20), (20, 255, 200))],
        }

        color_counts = {}

        for color_name, ranges in color_ranges.items():
            total_pixels = 0
            for lower, upper in ranges:
                mask = cv2.inRange(
                    hsv,
                    np.array(lower, dtype=np.uint8),
                    np.array(upper, dtype=np.uint8)
                )
                total_pixels += cv2.countNonZero(mask)

            color_counts[color_name] = total_pixels

        detected_color = max(color_counts, key=color_counts.get)

        print("Using bbox for color:", bbox)
        print("Color counts:", color_counts)
        print("Detected color:", detected_color)

        if color_counts[detected_color] == 0:
            return "unknown"

        return detected_color