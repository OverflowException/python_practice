import sys
import cv2
import math

if len(sys.argv) != 2:
    print("Usage: python" + sys.argv[0] + " [image]")
    sys.exit()

img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
blur_img_1 = cv2.GaussianBlur(img, (5, 5), sigmaX = 2, sigmaY = 2)
blur_img_2 = cv2.GaussianBlur(img, (5, 5), sigmaX = 2 * math.sqrt(2), sigmaY = 2 * math.sqrt(2))
dog_img = blur_img_2 - blur_img_1;

cv2.imshow("Dog", dog_img)
cv2.waitKey(0)
