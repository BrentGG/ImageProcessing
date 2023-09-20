import cv2 as cv
import imutils
import ctypes
import math

# Camera data
camHeight = 134  # in cm
camHorFOV = 64.8  # 69.3  # 58.8  # in degrees
camVerFOV = 51.3  # 53.5  # 45.8  # in degrees

z = 123.0  # use a set distance to the camera for now

if __name__ == '__main__':
    # Get screen info
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Get video capture
    cap = cv.VideoCapture(1)  # Change to 0 to use the built-in camera
    if not cap.isOpened():
        print("Could not open camera")
        exit(-1)

    # Get the facial detection cascade
    faceCascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_alt.xml")

    while True:
        # Read frame and detect face
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = imutils.resize(img, height=int(screensize[1] * 0.8))
        imgGrey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imgGrey = cv.equalizeHist(imgGrey)
        faces = faceCascade.detectMultiScale(imgGrey, 1.3, 5)

        img = cv.rectangle(img, ((int(len(img[0]) / 2)), int(len(img) / 2)), (int(len(img[0]) / 2) + 5, int(len(img) / 2) + 5), (0, 255, 0), 2)
        if len(faces) > 0:
            # Draw rectangle around face
            fx, fy, fw, fh = faces[0]
            img = cv.rectangle(img, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
            img = cv.rectangle(img, (fx + int(fw / 2), fy + int(fh / 2)), (fx + int(fw / 2) + 5, fy + int(fh / 2) + 5), (0, 255, 0), 2)

            # Calculate face position relative to camera
            halfX = math.tan(math.radians(camHorFOV/2)) * z
            x = (fx + (fw / 2) - (len(img[0]) / 2)) / (len(img[0]) / 2) * halfX
            halfY = math.tan(math.radians(camVerFOV/2)) * z
            y = (fy + (fh / 2) - (len(img) / 2)) / (len(img) / 2) * halfY
            y *= -1

            # Calculate pitch and yaw relative to camera
            yaw = math.degrees(math.atan(x / z))
            pitch = math.degrees(math.atan(y / z))

            print("x:{:6}   y:{:6}   z:{:6}   yaw:{:6}   pitch:{:6}".format(round(x, 1), round(y, 1), round(z, 1), round(yaw, 1), round(pitch, 1)))

        # Show frame
        cv.imshow('Turret', img)

        # Close when q is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

