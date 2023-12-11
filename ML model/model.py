import numpy as np
import os
import warnings
os.environ["TF_CCP_MIN_LOG_LEVEL"] = "1"
import tensorflow as tf
from tensorflow import keras


tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# warnings.filterwarnings('ignore')

def process_image(currImage):
    #declaring the different classes of possible brain tumor
    class_names=['glioma', 'meningioma', 'notumor', 'pituitary']

    #load
    try:
        model = keras.models.load_model(r"C:\Users\DittmanSeon\OneDrive - University of Wisconsin-Stout\Documents\GitHub\CS458_Brain_Tumor_Detection\ML model\my_model.keras") #change to new local location of the model

        img_path = currImage  # Full path to the image
        img = tf.keras.utils.load_img(
            img_path, target_size=(180, 180)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
    except Exception:
        pass

    #add confidence percentages to designated array
    if (class_names[np.argmax(score)] == "glioma"):
        glioma = (100 * np.max(score))
        return (glioma, 1)
    elif (class_names[np.argmax(score)] == "meningioma"):
        meningioma = (100 * np.max(score))
        return (meningioma, 2)
    elif (class_names[np.argmax(score)] == "notumor"):
        notumor = (100 * np.max(score))
        return (notumor, 0)
    elif (class_names[np.argmax(score)] == "pituitary"):
        pituitary = (100 * np.max(score))
        return (pituitary, 3)

