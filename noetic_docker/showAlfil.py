import cv2
import sys

"""
if (len(sys.argv) != 3 ):
    print("usage:   python3 ejemplo.y <window width> <window height>")
    exit(1)

width = sys.argv[1]
height = sys.argv[2]
print(width, height)
"""

im = cv2.imread("/home/shared_dir/alfil.png")
#im = cv2.resize(im, (int(width),int(height)) , interpolation = cv2.INTER_AREA)

winname = "imagen de un alfil"
cv2.namedWindow(winname)        # Create a named window
cv2.moveWindow(winname, 0,0)

cv2.imshow(winname,im)
cv2.waitKey(0)
cv2.destroyAllWindows()
