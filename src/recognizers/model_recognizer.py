import cv2
from ultralytics import YOLO
import logging


def recognize(model_file: str, filepath: str | list[str], verbose: bool):
    imgs = _load_imgs(filepath)
    model = YOLO(model_file)
    logging.info('start of the recognition of chart elements in the image')
    results = model.predict(source=imgs, verbose=verbose)
    return results

def _load_imgs(filepath: str | list[str]):
    logging.info('image loading has started')
    if type(filepath) is str:
        return cv2.imread(filepath)
    if type(filepath) is list:
        return [cv2.imread(file) for file in filepath]
    raise ValueError('expected str or list[str]')
