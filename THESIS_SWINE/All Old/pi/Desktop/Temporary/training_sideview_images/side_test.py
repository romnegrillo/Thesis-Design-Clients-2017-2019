import cv2

img=cv2.imread("./rgb_2019-01-22_21_12_33.475210.jpg")

cv2.imshow("test",img)

cv2.waitKey(0)
cv2.destroyAllWindows()
