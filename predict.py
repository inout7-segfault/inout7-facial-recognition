import os
import pickle

import face_recognition
import pandas as pd
from mtcnn.mtcnn import MTCNN
from database import get_student

FOLDER_PATH = os.getcwd()

roll_data = pd.read_csv("training/students.csv")

loaded_model = pickle.load(open("training/model.sav", "rb"))


def find_student(img):
    detector = MTCNN()
    faces = detector.detect_faces(img)

    for face in faces:
        box = face["box"]
        box = (box[1], box[0] + box[2], box[1] + box[3], box[0])
        encodings = face_recognition.face_encodings(img, [box])
        predictions = loaded_model.predict_proba(encodings)
        index = loaded_model.predict(encodings)
        student_details = get_student(int(index[0]))
        student_details["accuracy"] = predictions[0][index][0]

        return student_details
