Python Library actspotter
========================================

The `actspotter` is a library / tensorflow model for detecting activities. It allows to classify body activities in images or videos. The package is limited to videos and images with only one person by design.

The following classes are available: `none, pull_up_down, pull_up_none, pull_up_up, push_up_down, push_up_none, push_up_up`.

The package is currently in early development.

Future plans
~~~~~~~~~~~~~

Tensorflow model deployment will be integrated soon. Currently this package allows to classify push-ups and pull-ups. In future version kicks and others body activities will follow. 

It is also planned to provide a signal processing layer that allows to easily detect connected activites and count them. 

Another application will be to integrate with keyboard drivers so that activities could be used for controlling video games (e.g. by kicks).

Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/


Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.6

Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install actspotter


Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install actspotter


Example Usage
~~~~~~~~~~~~~

Requirement: cv2 (opencv) installed.

Classification of images:

.. code:: python

    import cv2
    import tensorflow as tf
    from actspotter import ImageClassifier, classify_image_input_dimension, class_names

    def _resize(frame, dim=classify_image_input_dimension):
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        return frame

    def _to_tf_array(frame, dim=classify_image_input_dimension):
        frame = _resize(frame, dim)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = tf.convert_to_tensor(frame, dtype=tf.float32)
        return frame

    images = [
        to_tf_array(cv2.imread("test.jpg")),
    ]
    
    print(class_names)
    print(image_classifier.classify_images(images))

Classification of a video:

.. code:: python

    import cv2
    import tensorflow as tf
    from actspotter import VideoClassifier, classify_image_input_dimension

    def _resize(frame, dim=classify_image_input_dimension):
        return frame

    def _to_tf_array(frame, dim=classify_image_input_dimension):
        frame = _resize(frame, dim)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = tf.convert_to_tensor(frame, dtype=tf.float32)
        return frame

    cap = cv2.VideoCapture(0)

    video_classifier = VideoClassifier(buffer_size=4)
    video_classifier.start()

    while cap.isOpened():
        ret, frame = cap.read()

        if ret == True:
            video_classifier.add_image(to_tf_array(frame))
            state = video_classifier.get_last_classification()
            print(state)

            frame = resize(frame, dim=(600, 600))
            cv2.putText(frame, f"{state}", (10, 40), 0, 2, 255)

            cv2.imshow("Frame", frame)

            waitkey = cv2.waitKey(25) & 0xFF

            if waitkey == ord("q"):
                break
                    
    video_classifier.exit()
    cap.release()
    cv2.destroyAllWindows()
