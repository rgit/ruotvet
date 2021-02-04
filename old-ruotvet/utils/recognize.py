import numpy as np
import easyocr
import random
import string
import cv2


class Recognizer:
    @staticmethod
    def _normalize_image(image):
        normalized_planes = []
        for plane in cv2.split(cv2.imread(image, -1)):
            bg_img = cv2.medianBlur(cv2.dilate(plane, np.ones((7, 7), np.uint8)), 21)
            normalized_plane = cv2.normalize(255 - cv2.absdiff(plane, bg_img), alpha=0, beta=255,
                                             norm_type=cv2.NORM_MINMAX,
                                             dtype=cv2.CV_8UC1, dst=np.array([]))
            normalized_planes.append(normalized_plane)
        return cv2.merge(normalized_planes)

    @staticmethod
    def _threshold_image(image):
        return cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    @staticmethod
    def _extract_text(image):
        reader = easyocr.Reader(["ru"])
        chunks, text = reader.readtext(image), ""
        for chunk in chunks:
            text = text + chunk[1]
        return text

    @staticmethod
    def _draw_boxes(image, details, accuracy_threshold=30):
        total_boxes = len(details["text"])
        for sequence_number in range(total_boxes):
            if int(details["conf"][sequence_number]) > accuracy_threshold:
                (x, y, w, h) = (details["left"][sequence_number], details["top"][sequence_number],
                                details["width"][sequence_number], details["height"][sequence_number])
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        filename = "".join(
            random.choice(string.ascii_uppercase + string.ascii_letters + string.digits) for _ in range(12))
        cv2.imwrite(f"{filename}.png", image)
        return f"{filename}.png"

    def get_text_from_image(self, image_path: str, threshold: bool = False):
        if threshold:
            return self._extract_text(self._threshold_image(self._normalize_image(image_path)))
        else:
            return self._extract_text(self._normalize_image(image_path))
