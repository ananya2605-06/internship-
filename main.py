import face_recognition
import cv2
import numpy as np
from datetime import datetime
import pyttsx3 as text
import smtplib

engine = text.init()

print("Capturing video frame...")
video_capture = cv2.VideoCapture(0)

# # # Load a sample picture and learn how to recognize it.
img081 = face_recognition.load_image_file("Images/1RN22CD055_Nishvika.jpg")
img_081_encoding = face_recognition.face_encodings(img081)[0]
# #
# # # Load a sample picture and learn how to recognize it.
img082 = face_recognition.load_image_file("Images/1RN22CD014_ANANYA.jpg")
img_082_encoding = face_recognition.face_encodings(img082)[0]
# #
# # #Load a sample picture and learn how to recognize it.
img027 = face_recognition.load_image_file("Images/1RN22CD027_DHANYA.jpg")
img_027_encoding = face_recognition.face_encodings(img027)[0]
# #
#Load a sample picture and learn how to recognize it.
img015 = face_recognition.load_image_file("Images/1RN22CD015_ANJU.jpg")
img_015_encoding = face_recognition.face_encodings(img015)[0]

##Load a sample picture and learn how to recognize it.
img022 = face_recognition.load_image_file("Images/1RN22CD022_CHANDANA.jpg")
img_022_encoding = face_recognition.face_encodings(img022)[0]

#Load a sample picture and learn how to recognize it.
img010 = face_recognition.load_image_file("Images/1RN22CD010_SHYLA.jpg")
img_010_encoding = face_recognition.face_encodings(img010)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [img_010_encoding, img_022_encoding, img_015_encoding,img_027_encoding,img_082_encoding,img_081_encoding]
known_face_names = ["Shyla", "Chandana", "Anju","Dhanya","Ananya","Nishvika"]

# Initialization variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def intruder():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('miniproject2456@gmail.com', 'dkiw vfet bipx krih')
    server.sendmail('miniproject2456@gmail.com', 'miniproject2456@gmail.com', 'Intruder detected')
    print("mail sent")

def markattendance(name):
    with open('attendance.cs','r+') as f:
        mydatalist = f.readlines()
        namelist = []
        for line in mydatalist:
            entry = line.split(',')
            namelist.append(entry[0])

        if name not in namelist:
            
            timestr = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
            f.writelines(f'\n{name},{timestr}')
            engine.say("Welcome" + name)
            engine.runAndWait()

while True:
    print("Processing video frame...")
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, we can use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                markattendance(name)
                print("Face recognized as",name)
            else:
                intruder()

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image in frame with the bounding box & name
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()