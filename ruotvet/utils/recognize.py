# from PIL import Image, ImageFilter, ImageEnhance
# import pytesseract
# import cv2


# image = Image.open("example.png")

# image = image.filter(ImageFilter.GR)
# im = im.filter(ImageFilter.MedianFilter())
# enhancer = ImageEnhance.Contrast(im)
# im = enhancer.enhance(2)
# # im = im.convert("1")
# im.save("clear-example.png")


from PIL import Image
import numpy as np
import pytesseract
import cv2


def normalize_image(image):
    normalized_planes = []
    for plane in cv2.split(image):
        bg_img = cv2.medianBlur(cv2.dilate(plane, np.ones((7, 7), np.uint8)), 21)
        normalized_plane = cv2.normalize(255 - cv2.absdiff(plane, bg_img), alpha=0, beta=255, norm_type=cv2.NORM_MINMAX,
                                         dtype=cv2.CV_8UC1, dst=np.array([]))
        normalized_planes.append(normalized_plane)
    return cv2.merge(normalized_planes)


def threshold_image(image):
    return cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


def extract_text(image):
    return pytesseract.image_to_data(Image.open("clear-example.png"), output_type=pytesseract.Output.DICT,
                                     config=r"--oem 3 --psm 6", lang="rus")


image = cv2.imread("example.png", -1)


def draw_boxes(image, details, accuracy_threshold = 30):
    """
    This function takes three argument as
    input. it draw boxes on text area detected
    by Tesseract. it also writes resulted image to
    your local disk so that you can view it.
    :param image: image
    :param details: dictionary
    :param threshold_point: integer
    :return: None
    """
    total_boxes = len(details['text'])
    for sequence_number in range(total_boxes):
        if int(details['conf'][sequence_number]) > accuracy_threshold:
            (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number],
                            details['width'][sequence_number], details['height'][sequence_number])
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # saving image to local
    cv2.imwrite('captured_text_area.png', image)
    # display image
    cv2.imshow('captured text', image)
    # Maintain output window until user presses a key
    cv2.waitKey(0)
    # Destroying present windows on screen
    cv2.destroyAllWindows()


draw_boxes(threshold_image(normalize_image(image)), extract_text(threshold_image(normalize_image(image))))


# text = pytesseract.image_to_data(Image.open("clear-example.png"), output_type=pytesseract.Output.DICT,
#                                  config=r"--oem 3 --psm 6", lang="rus")
# print(text)
#
# import cv2 as cv
# import matplotlib.pyplot as plt
# filename = "example.png"
# img = cv.imread(filename)
# cv.imshow("dst", img)
# cv.waitKey(0)

#
# import cv2
# import numpy as np
#
# img = cv2.imread("example.png")
#
# result = np.ones(img.shape[:2], np.uint8) * 255
# for channel in cv2.split(img):
#     canvas = np.ones(img.shape[:2], np.uint8) * 255
#     contours = cv2.findContours(255 - channel, cv2.RETR_LIST,
#                                 cv2.CHAIN_APPROX_SIMPLE)[0]
#     # size threshold may vary per image
#     contours = [cnt for cnt in contours if cv2.contourArea(cnt) <= 100]
#     cv2.drawContours(canvas, contours, -1, 0, -1)
#     result = result & (canvas | channel)
#
# cv2.imwrite("result.png", result)



# import csv
# import cv2
# import pytesseract
#
#
# def pre_processing(image):
#     """
#     This function take one argument as
#     input. this function will convert
#     input image to binary image
#     :param image: image
#     :return: thresholded image
#     """
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # converting it to binary image
#     threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#     # saving image to view threshold image
#     cv2.imwrite('thresholded.png', threshold_img)
#
#     cv2.imshow('threshold image', threshold_img)
#     # Maintain output window until
#     # user presses a key
#     cv2.waitKey(0)
#     # Destroying present windows on screen
#     cv2.destroyAllWindows()
#
#     return threshold_img
#
#
# def parse_text(threshold_img):
#     """
#     This function take one argument as
#     input. this function will feed input
#     image to tesseract to predict text.
#     :param threshold_img: image
#     return: meta-data dictionary
#     """
#     # configuring parameters for tesseract
#     tesseract_config = r'--oem 3 --psm 6'
#     # now feeding image to tesseract
#     details = pytesseract.image_to_data(threshold_img, output_type=pytesseract.Output.DICT,
#                                         config=tesseract_config, lang='eng')
#     return details
#
#
# def draw_boxes(image, details, threshold_point):
#     """
#     This function takes three argument as
#     input. it draw boxes on text area detected
#     by Tesseract. it also writes resulted image to
#     your local disk so that you can view it.
#     :param image: image
#     :param details: dictionary
#     :param threshold_point: integer
#     :return: None
#     """
#     total_boxes = len(details['text'])
#     for sequence_number in range(total_boxes):
#         if int(details['conf'][sequence_number]) > threshold_point:
#             (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number],
#                             details['width'][sequence_number], details['height'][sequence_number])
#             image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     # saving image to local
#     cv2.imwrite('captured_text_area.png', image)
#     # display image
#     cv2.imshow('captured text', image)
#     # Maintain output window until user presses a key
#     cv2.waitKey(0)
#     # Destroying present windows on screen
#     cv2.destroyAllWindows()
#
#
# def format_text(details):
#     """
#     This function take one argument as
#     input.This function will arrange
#     resulted text into proper format.
#     :param details: dictionary
#     :return: list
#     """
#     parse_text = []
#     word_list = []
#     last_word = ''
#     for word in details['text']:
#         if word != '':
#             word_list.append(word)
#             last_word = word
#         if (last_word != '' and word == '') or (word == details['text'][-1]):
#             parse_text.append(word_list)
#             word_list = []
#
#     return parse_text
#
#
# def write_text(formatted_text):
#     """
#     This function take one argument.
#     it will write arranged text into
#     a file.
#     :param formatted_text: list
#     :return: None
#     """
#     with open('resulted_text.txt', 'w', newline="") as file:
#         csv.writer(file, delimiter=" ").writerows(formatted_text)
#
#
# if __name__ == "__main__":
#     # reading image from local
#     image = cv2.imread("example.png")
#     # calling pre_processing function to perform pre-processing on input image.
#     thresholds_image = pre_processing(image)
#     # calling parse_text function to get text from image by Tesseract.
#     parsed_data = parse_text(thresholds_image)
#     # defining threshold for draw box
#     accuracy_threshold = 30
#     # calling draw_boxes function which will draw dox around text area.
#     draw_boxes(thresholds_image, parsed_data, accuracy_threshold)
#     # calling format_text function which will format text according to input image
#     arranged_text = format_text(parsed_data)
#     # calling write_text function which will write arranged text into file
#     write_text(arranged_text)
