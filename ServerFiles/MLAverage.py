import sys
import os
import MLModel as ML

sys.path
sys.executable

#load in a folder of images
# ughfolder = r"C:\Users\steph\PycharmProjects\machineLearning\testing\example" #change to user selected folder
#parse through images in folder

def ML_nice_results(folder_path):
    results = []
    for img_filename in os.listdir(folder_path):
        if img_filename.endswith(".jpg"):
            img_path = os.path.join(folder_path, img_filename)  # Full path to the image
            #img = tf.keras.utils.load_img(
            #    img_path, target_size=(180, 180)
            #)
            result = ML.process_image(currImage=img_path)
            results.append(result)

    return results

def ML_get_folder_averages(results):
    chanceN = 0  # 0
    nummaN = 0
    chanceG = 0  # 1
    nummaG = 0
    chanceM = 0  # 2
    nummaM = 0
    chanceP = 0  # 3
    nummaP = 0
    for result in results:
        chance, typaC = result

        typaC = int(typaC)
        # print(chance, typaC)

        if typaC == 0:
            chanceN += chance
            nummaN += 1
        elif typaC == 1:
            chanceG += chance
            nummaG += 1
        elif typaC == 2:
            chanceM += chance
            nummaM += 1
        elif typaC == 3:
            chanceP += chance
            nummaP += 1
        else:
            print("You messed up!")

    def myAverage(x, y):
        try:
            return x/y, y
        except Exception:
            # print(Exception)
            return 0, 0

    averageN = myAverage(chanceN, nummaN)
    averageG = myAverage(chanceG, nummaG)
    averageM = myAverage(chanceM, nummaM)
    averageP = myAverage(chanceP, nummaP)

    # return averageN, averageG, averageM, averageP
    # it should look like this: x% no tumor based on y images, x% glioma based on y images, etc.
    myResult = str(averageN) + r"% no tumor based on " + str(nummaN) + r" images, " + str(averageG) + r"% glioma based on " + str(nummaG) + " images, " + str(averageM) + r"% meningioma based on " + str(nummaM) + " images, " + str(averageP) + r"% pituitary based on " + str(nummaP) + " images."
    return myResult
