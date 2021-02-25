from string import ascii_letters, ascii_uppercase, digits
from typing import Optional, List, Dict, Union
from pytesseract import image_to_data, Output
from ruotvet.types import File
from numpy import ndarray
from random import choice
import cv2


class Preprocess:
    @staticmethod
    def grayscale(image: ndarray) -> ndarray:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def canny(image: ndarray) -> ndarray:
        return cv2.Canny(image, 100, 200)


class OCR:
    def recognize(self, image: str, language_code: str = "rus") -> Optional[Dict[Union[str, int], List]]:
        """
        This function makes OCR and returns image data.
        :param image: The image path for OCR.
        :param language_code: The language code for OCR. By default, is Russian.
        """
        return image_to_data(Preprocess.grayscale(cv2.imread(image)), output_type=Output.DICT, lang=language_code,
                             config="--oem 3 --psm 6")

    def show_boxes(self, image: str, path: str = None, format: str = "png", language_code: str = None) -> File:
        """
        This function makes OCR and returns an image file with boxes around founded text.
        :param image: The image path for OCR.
        :param path: Saving path for an image file. Set empty for saving in the current path.
        :param format: Format for an image file. By default, is png.
        :param language_code: The language code for OCR.
        """
        data = self.recognize(image, language_code)
        image, result = cv2.imread(image), None
        for i in range(len(data["text"])):
            if int(data["conf"][i]) > 60:
                (x, y, w, h) = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
                result = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        filename = "".join(choice(ascii_uppercase + ascii_letters + digits) for _ in range(15))
        path = f"{path}/{filename}.{format}" if path else f"{filename}.{format}"
        cv2.imwrite(path, result)
        return File(path=path, format=format)
