import pandas as pd
import os
import cv2
import numpy as np
import cvlib as cv
from collections import defaultdict
import random
from tqdm import tqdm
from .commonwords import COMMON_WORDS
from copy import copy

class ImageIndexer:
    _common_words = COMMON_WORDS

    def __init__(self, frames_per_image=100, max_frames=10000):
        self._max_frames = max_frames
        self._frames_per_image = frames_per_image

    def _extract_frames(self):
        self._vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        max_frames = int(self._vidcap.get(cv2.CAP_PROP_POS_FRAMES))
        self._vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
        n_frames = min(max_frames, self._max_frames)
        for frame in tqdm(range(n_frames)):
            success, image = self._vidcap.read()
            if not success:
                break
            if (frame % self._frames_per_image == 0):
                yield image, frame

    def classify_video(self, videopath):
        self._vidcap = cv2.VideoCapture(videopath.path)
        for image, frame_number in self._extract_frames():
            bounding_boxes, words, _conf = cv.detect_common_objects(image) 
        for bb, word in zip(bounding_boxes, words):
            yield word, self._get_sub_image(image, bb), frame_number

    def _get_sub_image(self, image, bb):
        bb = [box_val if box_val >= 0 else 0 for box_val in bb]
        return image[bb[1]:bb[3], bb[0]:bb[2]]

    def get_generator(self):
        for word, frame_info in self._image_indices.items():
            for frame_number, bb in frame_info:
                yield word, self._get_sub_image(self._images[frame_number], bb), frame_number
