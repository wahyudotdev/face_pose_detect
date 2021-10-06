import cv2
import imutils
import time
import serial

is_arduino_ready = False
try:
    arduino = serial.Serial('COM5', 9600)
    is_arduino_ready = True
except:
    is_arduino_ready = False

time.sleep(2)
print("Connection to arduino...")

cascPath = 'haarcascade_frontalface_default.xml'

# Create the Haar Cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Read the Video
video_capture = cv2.VideoCapture(0)
time.sleep(1)
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Resize the Frame to improve speed
    frame = imutils.resize(frame, width=450)

    # Convert to Gray-Scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(25, 25)
    )

    # Draw a rectangle around the Faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting Frame
    cv2.imshow('Video', frame)
    xx = int(x+(x+h))/2
    yy = int(y+(y+w))/2

    print (xx)
    print (yy)

    center = (xx,yy)

    print("Center of Rectangle is :", center)
    data = "X{0:d}Y{1:d}Z".format(int(xx), int(yy))
    print ("output = '" +data+ "'")
    if is_arduino_ready:
        arduino.write(data)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()