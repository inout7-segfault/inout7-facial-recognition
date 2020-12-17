import csv
import os
import pickle

import pandas as pd
import face_recognition
import numpy as np
from mtcnn.mtcnn import MTCNN
from PIL import Image
from sklearn.svm import SVC

# Path to directory containing images to train
PATH = "/home/prajith_v/Pictures/pic_to_train_2"

# Filename to save model as
MODEL_FILENAME = "model.sav"

# Filename to save students' names
CSV_FILE = "students.csv"

names = os.listdir(PATH)
mapping = {v: i for i, v in enumerate(names)}


pd_csv = pd.DataFrame(
    {"Roll": [mapping[i] for i in mapping.keys()], "Name": [i for i in mapping.keys()]}
)
pd_csv.to_csv(CSV_FILE, sep=",")

detector = MTCNN()

labels = []
face_images = []
encodings = []
for folder in names:
    path_folder = f"{PATH}/{folder}"
    print(f"Training {path_folder}")

    for image in os.listdir(path_folder):
        img = np.array(Image.open(f"{path_folder}/{image}"))
        faces = detector.detect_faces(img)

        if len(faces) != 0:
            face_images.append(img)
            box = faces[0]["box"]
            box = (box[1], box[0] + box[2], box[1] + box[3], box[0])
            encodings.append(face_recognition.face_encodings(img, [box]))
            labels.append(mapping[folder])

        else:
            print(f"{path_folder}/{image} not detected")

face_image_encodings = np.array(encodings)
face_image_labels = np.array(labels)

model = SVC(kernel="sigmoid", probability=True)
model.fit(
    np.reshape(face_image_encodings, (face_image_encodings.shape[0], 128)),
    face_image_labels,
)

model.score(
    np.reshape(face_image_encodings, (face_image_encodings.shape[0], 128)),
    face_image_labels,
)

pickle.dump(model, open(MODEL_FILENAME, "wb"))
