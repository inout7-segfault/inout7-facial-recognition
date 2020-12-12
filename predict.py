import pickle,face_recognition,imageio
import pandas as pd
from mtcnn.mtcnn import MTCNN
from sklearn.svm import SVC

FOLDER_PATH = os.getcwd()

roll_data = pd.read_csv("Training/students.csv")

loaded_model = pickle.load(open("Training/model.sav", "rb"))


def find_student(img):
    detector = MTCNN()
    faces = detector.detect_faces(img)

    for face in faces:
        box = face["box"]
        box = (box[1], box[0] + box[2], box[1] + box[3], box[0])
        encodings = face_recognition.face_encodings(img, [box])
        predictions = loaded_model.predict_proba(encodings)
        index = loaded_model.predict(encodings)
        temp = predictions[0]

        print(predictions[0][index][0])
        print(roll_data[roll_data["Roll"]==index[0]]["Name"].values)
        
        return index,roll_data[roll_data["Roll"]==index[0]]["Name"].values