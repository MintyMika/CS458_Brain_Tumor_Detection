import numpy as np
import os
os.environ["TF_CCP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf
from tensorflow import keras

#declaring the different classes of possible brain tumor
class_names=['glioma', 'meningioma', 'notumor', 'pituitary']

#load model
model = keras.models.load_model(r"C:\Users\DittmanSeon\OneDrive - University of Wisconsin-Stout\Documents\GitHub\CS458_Brain_Tumor_Detection\ML model\my_model.keras") #change to new local location of the model

#create arrays to store percentage confidence
glioma=[]
meningioma=[]
notumor=[]
pituitary=[]

#load in a folder of images
folder = r"C:\Users\DittmanSeon\PycharmProjects\capstone\test" #change to user selected folder

#parse through images in folder
for img_filename in os.listdir(folder):
    if img_filename.endswith(".jpg"):
        img_path = os.path.join(folder, img_filename)  # Full path to the image
        img = tf.keras.utils.load_img(
            img_path, target_size=(180, 180)
        )
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        #add confidence percentages to designated array
        if (class_names[np.argmax(score)] == "glioma"):
            glioma.append(100 * np.max(score))
        elif (class_names[np.argmax(score)] == "meningioma"):
            meningioma.append(100 * np.max(score))
        elif (class_names[np.argmax(score)] == "notumor"):
            notumor.append(100 * np.max(score))
        elif (class_names[np.argmax(score)] == "pituitary"):
            pituitary.append(100 * np.max(score))
        #find average percentage of different arrays
        if (len(glioma) > 0):
            global g
            g = sum(glioma) / len(glioma)
        elif (len(glioma) == 0):
            g = 0
        if(len(meningioma) > 0):
            global m
            m = sum(meningioma) / len(meningioma)
        elif (len(meningioma) == 0):
            m = 0
        if (len(notumor) > 0):
            global nt
            nt = sum(notumor) / len(notumor)
        elif (len(notumor) == 0):
            nt = 0
        if (len(pituitary) > 0):
            global p
            p = sum(pituitary) / len(pituitary)
        elif (len(pituitary) == 0):
            p = 0
#write results to text doc
with open('results.txt', 'a') as f:
    f.write("Results:glioma- {:.2f} percent confident based on {} images, meningioma- {:.2f} percent confident based on {} images, no tumor- {:.2f} percent confident based on {} images,pituitary- {:.2f} percent confident based on {} images. \n"
        .format(g,len(glioma),m,len(meningioma),nt,len(notumor),p,len(pituitary)))


