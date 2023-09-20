import cv2 as cv
import imutils
import ctypes

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

        if len(faces) > 0:
            # Draw rectangle around face
            fx, fy, fw, fh = faces[0]
            img = cv.rectangle(img, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
            # Estimate mouth position and size and draw rectangle around it
            #mw, mh = int(fw * 0.5), int(fw * 0.1)
            #mx, my = int((fx + fw / 2) - (mw / 2)), int((fy + fh * 0.8) - (mh / 2))
            #img = cv.rectangle(img, (mx, my), (mx + mw, my + mh), (255, 0, 0), 2)

        # Show frame
        cv.imshow('Turret', img)

        # Close when q is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

