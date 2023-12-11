import os
import model as ML


#load in a folder of images
folder = r"C:\\Users\\DittmanSeon\\PycharmProjects\\capstone\\test" #change to user selected folder
#parse through images in folder

def ML_nice_results(folder_path):
    results = []
    for img_filename in os.listdir(folder):
        if img_filename.endswith(".jpg"):
            img_path = os.path.join(folder, img_filename)  # Full path to the image
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

    return averageN, averageG, averageM, averageP

# Debugging
results = ML_nice_results(folder)
print(ML_get_folder_averages(results))



