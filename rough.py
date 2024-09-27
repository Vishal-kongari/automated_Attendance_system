import cv2
from datetime import datetime
# Load the pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier('face.xml')

# Start video capture from the default webcam (index 0)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale (face detection works on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the number of faces detected on the frame
    face_count = len(faces)
    cv2.putText(frame, f'Faces: {face_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Also print the count of faces in the terminal
    print(f'Number of faces detected: {face_count}')


    # Show the frame
    cv2.imshow('Face Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print(datetime.now().hour)
# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
