import cv2
from ultralytics import YOLO


def recognize(model_file: str, filepath: str | list[str]):
    imgs = _load_imgs(filepath)
    # print(f'shape: {imgs[0].shape}')
    # print(f'type: {type(imgs[0])}')
    # print(f'sub: {imgs[0][8:600, 1:500].shape}')
    model = YOLO(model_file)
    results = model.predict(source=imgs)
    return results

def _load_imgs(filepath: str | list[str]):
    if type(filepath) is str:
        return cv2.imread(filepath)
    if type(filepath) is list:
        return [cv2.imread(file) for file in filepath]
    raise ValueError('expected str or list[str]')
