from time import strftime

import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

attendance=0
cred = credentials.Certificate("C:/Users/Rammohan/projects/face_attendance_system/serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://bus-safety-automation-default-rtdb.firebaseio.com/",
    "storageBucket":"bus-safety-automation.appspot.com"
})


face_cascade = cv2.CascadeClassifier('face.xml')

bucket=storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
background = cv2.imread("C:/Users/Rammohan/projects/face_attendance_system/background.png")

Path_images=os.listdir("C:/Users/Rammohan/projects/face_attendance_system/images")
img_mode=[]
for i in Path_images:
    img_mode.append(cv2.imread(os.path.join("C:/Users/Rammohan/projects/face_attendance_system/images",i)))

file=open('encoder.p','rb')
encodeList_withids=pickle.load(file)
file.close()
encodelist,studentids=encodeList_withids


mode=0
counter=0
id=-1
imgstu=[]




#print(studentids)
while True:
    _,img=cap.read()
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_cur_frame=face_recognition.face_locations(imgs) #location of face in imgs
    encode_cur_face=face_recognition.face_encodings(imgs,face_cur_frame) #encoding of face given from face_cue_frame



    background[162:162+480,55:55+640]=img
    background[44:44+633,808:808+414]=img_mode[mode]
    #cv2.imshow("dispay",img)
    if face_cur_frame:
        for encodeface,faceloc in zip(encode_cur_face,face_cur_frame):
            matches=face_recognition.compare_faces(encodelist,encodeface)
            face_dis=face_recognition.face_distance(encodelist,encodeface)
            #print("matches:",matches)
            #print("face_dis:",face_dis)
            match_index=np.argmin(face_dis)
            #print(match_index)
            if matches[match_index]:

                id = studentids[match_index]
                if counter==0:
                    cvzone.putTextRect(background,"Loading",(275,400))
                    cv2.imshow("face attendance",background)
                    cv2.waitKey(1)
                    counter=1
                    mode=1
        if counter!=0:
            if counter==1:
                #data from data base
                studentinfo= db.reference(f'Students/{id}').get()
                #print(studentinfo)
                #data from storage
                blob= bucket.get_blob(f'C:/Users/Rammohan/projects/face_attendance_system/data/{id}.png')
                #print(blob)
                arr=np.frombuffer(blob.download_as_string(),np.uint8)  #converting student id img
                imgstu= cv2.imdecode(arr,cv2.COLOR_BGRA2RGB)

                #update attendance
                datetime_obj=datetime.strptime(studentinfo["last_attendance_time"],
                                               "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now()-datetime_obj).total_seconds()
                #print(secondsElapsed)
                if secondsElapsed > 5*60:
                    ref=db.reference(f'Students/{id}')

                    ref.child("last_attendance_time").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                else:
                    mode=3
                    counter =0
                    background[44:44 + 633, 808:808 + 414] = img_mode[mode]



            if mode!=3:


                if 20<counter<30:
                    mode=2
                    background[44:44 + 633, 808:808 + 414] = img_mode[mode]



                if counter<=20:
                    cv2.putText(background,str(studentinfo["branch"]),(1006,550),cv2.FONT_HERSHEY_COMPLEX,
                                    1,(255,255,255),1)
                    cv2.putText(background, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX,
                                    0.5, (255, 255, 255), 1)
                    (w,h),_=cv2.getTextSize(studentinfo["name"],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    oset=(414-w)//2 #414 is the total width od the display window
                    cv2.putText(background, str(studentinfo["name"]), (808+oset, 445), cv2.FONT_HERSHEY_COMPLEX,
                                    1, (0, 0, 0), 1)

                    background[175:175+216,909:909+216]=imgstu

                counter+=1
                if counter>=30:
                    #message to parent

                    counter=0
                    mode=0
                    studentinfo=[]
                    imgstu=[]
                    background[44:44 + 633, 808:808 + 414] = img_mode[mode]
    else:
        mode=0
        counter=0

    cv2.imshow("face attendance",background)
    cv2.waitKey(1)

