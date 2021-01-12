import cv2

cap=cv2.VideoCapture(0)

try:
    while 1:
            ret,img=cap.read()

            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            blur=cv2.GaussianBlur(gray,(3,3),0)

            cv2.imshow("capture",gray)

            if cv2.waitKey(1) == ord("q"):
                break


except:
    cap.release()
