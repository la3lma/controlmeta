import cv2

haar_cascade_home='/usr/local/Cellar/opencv/2.4.6.1/share/OpenCV/haarcascades/'

def hc(p):
    return haar_cascade_home + p

def detect(path):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier(hc("haarcascade_frontalface_alt.xml"))
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def box(rects, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite('detected.jpg', img);

rects, img = detect("../tests/images/lena1.jpeg")
box(rects, img)

