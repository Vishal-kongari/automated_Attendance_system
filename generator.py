from copyreg import pickle

import cv2
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("C:/Users/Rammohan/projects/face_attendance_system/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://bus-safety-automation-default-rtdb.firebaseio.com/",
    "storageBucket":"bus-safety-automation.appspot.com"
})

Path_faces=os.listdir("C:/Users/Rammohan/projects/face_attendance_system/data")
#print(Path_faces)
img_faces=[]
studentid=[]


path="C:/Users/Rammohan/projects/face_attendance_system/data"

for i in Path_faces:
    img_faces.append(cv2.imread(os.path.join(path,i)))#faces are taken from images
    #to keep ids
    studentid.append(os.path.splitext(i)[0])

    fileName=f'{path}/{i}'
    bucket=storage.bucket()
    blob=bucket.blob(fileName)
    blob.upload_from_filename(fileName)









def findEncoding(imagesList):
    encode=[]
    for img in imagesList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode.append(face_recognition.face_encodings(img)[0])
    return encode
encodeList=findEncoding(img_faces)
encodeList_with_ids=[encodeList,studentid]
#print(encodeList_with_ids)
file=open("encoder.p",'wb')
pickle.dump(encodeList_with_ids,file)
file.close()

