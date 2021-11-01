import os
import time
import threading
import logging
from pathlib import Path
import json
import numpy as np
import tensorflow as tf

current_directory = Path(__file__).parent.absolute()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s: %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)

#
# Parameters 
#
classify_image_height = 150
classify_image_width = 150
classify_image_input_dimension=(classify_image_height, classify_image_width)
model_path = os.path.join(current_directory, './model')
model_path_environ_key = 'ACTSPOTTER_TF_MODEL_PATH'
model_path_environ = os.environ.get(model_path_environ_key)

if model_path_environ != None and len(model_path_environ) > 0:
    model_path = model_path_environ
else:
    logging.info(f'Model path {model_path_environ_key} not set. Using {model_path}')

#
# Loading the model 
#
logging.info(f'[ ] Loading model from {model_path}')
model = tf.keras.models.load_model(model_path)
logging.info('[x] Model loaded')

model_meta_path = os.path.join(model_path, 'meta.json')
with open(model_meta_path) as f:
    meta = json.load(f)
    classes = meta['classes']
    class_names = [classes[c] for c in sorted(classes.keys())]
    logging.info(f'Classes: {class_names}')

#
# Image classification 
#
class ImageClassifier():

    def classify_images(self, images):
        """Classifies a list of images."""
        if len(images) == 0:
            return 'none'

        if len(images) > 32:
            raise Exception('max_32_images_allowed_in_buffer')

        x = np.stack(images, axis=0)

        res = model.predict(x)
        
        return [class_names[np.argmax(r, axis=0)] for r in res]

#
# Video classification 
#
class VideoClassifier(threading.Thread):

    def __init__(self, callback_function = None, debug = False, buffer_size = 4):
        """Initialises the class"""
        threading.Thread.__init__(self)
        self.callback_function = callback_function
        self.image_buffer = []
        self.image_classifier = ImageClassifier()
        self.closed = False
        self.debug = debug
        self.last_classification_votes = ['none']
        self.image_buffer = []
        self.buffer_size = buffer_size
        self.lock = threading.Lock()

    def run(self):
        """Regularly runs the classification process in background"""
        while not self.closed:

            self.lock.acquire()
            if len(self.image_buffer) < self.buffer_size:
                self.lock.release()
                time.sleep(0.001)
                continue

            images = [image for image, _ in self.image_buffer]
            self.image_buffer = []
            self.lock.release()

            self.last_classification_votes = self.image_classifier.classify_images(images)
            
            if self.callback_function != None:
                self.callback_function(self.last_classification_votes)

    def exit(self):
        """Stops the video classification"""
        self.closed = True

    def add_image(self, image):
        """Adds an image to be classified"""

        self.lock.acquire()
        self.image_buffer.append((image, time.time()))

        if self.buffer_size >= 0 and len(self.image_buffer) > self.buffer_size:
            self.image_buffer = self.image_buffer[:-1*(self.buffer_size)]

        if len(self.image_buffer) > 32:
            self.image_buffer = self.image_buffer[:-32]

        self.lock.release()

    def get_last_classification_votes(self):
        """Returns the last classification votes of the last provided images"""
        return self.last_classification_votes

    def get_last_classification(self):
        """Returns the classification of the last provided images in the buffer selected by max votes."""
        classification_votes = self.get_last_classification_votes()
        last_classification = max(set(classification_votes), key = classification_votes.count)
        
        if self.debug:
            logging.info(f'Classification: {last_classification}. Votes: {classification_votes}')

        return last_classification