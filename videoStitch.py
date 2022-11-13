import cv2
from queue import Queue
import threading


def camPreview(previewName, camID, q):    # Function to start camera and get live input
    print("Camera ", camID, " is starting")
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)

    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        q.put(frame)                       # Share frame with other threads
        cv2.waitKey(100)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)


def stitch(q):                            # Function to stitch two frames
    while True:
        cv2.waitKey(100)

        print("Starting stitching...")

        frame1 = q.get()                  # Receive frames from other threads
        frame2 = q.get()
        print(q.qsize())
        imgs = [frame1, frame2]

        stitchy = cv2.Stitcher.create()
        (dummy, output) = stitchy.stitch(imgs)

        print(cv2.Stitcher_ERR_NEED_MORE_IMGS)

        if dummy != cv2.STITCHER_OK:
            print("Stitching ain't successful. Please adjust the cameras !!!")
            print()
            continue
        else:
            print("Stitching successful !!!")
            print()

        # final output
        cv2.imshow('Final result', output)


q = Queue()


t1 = threading.Thread(target = camPreview, args =("Camera 1", 0, q, ))   # Taking video input from Camera 1
t2 = threading.Thread(target = camPreview, args =("Camera 2", 1, q, ))   # Taking video input from Camera 2
t3 = threading.Thread(target = stitch, args =(q, ))                      # Stitches two videos


t1.start()
t2.start()
t3.start()