import cv2
import numpy as np
import easyocr

reader = easyocr.Reader(['ru','en'])

def recognize_text(img: np.ndarray) -> str:
    preproc_img = _preprocessing(img)
    text: list[str] = reader.readtext(preproc_img, detail=0)
    text = ' '.join(text)
    print(f"text: {text}")
    return text

def _sharpen(img: np.ndarray):
    sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(img, -1, sharpen_filter)

def _show_image(image, text='image'):
    cv2.imshow(text, image)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()

def _preprocessing(image: np.ndarray, sharpenFilter = False, showFlag = False):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
    sharpen = cv2.GaussianBlur(gray_image, (0, 0), 3)
    sharpen = cv2.addWeighted(gray_image, 1, sharpen, -0.5, 0)

    if sharpenFilter:
        gray_image = _sharpen(sharpen)
    
    if showFlag:
        _show_image(gray_image, 'res')

    return gray_image

def sub_image(image: np.ndarray, xyxy: tuple):
    x1, y1, x2, y2 = tuple(map(lambda x: int(round(x)), xyxy))
    return image[y1:y2, x1:x2]