import pygame
import Image
from pygame.locals import *
import sys

import opencv
#this is important for capturing/displaying images
from opencv import highgui
from opencv.highgui import *
from opencv.cv import *

camera = highgui.cvCreateCameraCapture(0)
def detect(image):
    image_size = cvGetSize(image)

    # create grayscale version
    grayscale = cvCreateImage(image_size, 8, 1)
    cvCvtColor(image, grayscale, CV_BGR2GRAY)

    # create storage
    storage = cvCreateMemStorage(0)
    cvClearMemStorage(storage)

    # equalize histogram
    cvEqualizeHist(grayscale, grayscale)

    # detect objects
    cascade = cvLoadHaarClassifierCascade('haarcascade_frontalface_alt.xml', cvSize(1,1))
    faces = cvHaarDetectObjects(grayscale,
            cascade,
            storage,
            1.2,
            2,
            CV_HAAR_DO_CANNY_PRUNING,
            cvSize(50, 50))

    if faces.total > 0:
        print '=> face detected!'
        for i in faces:
            cvRectangle(image, cvPoint( int(i.x), int(i.y)),
                         cvPoint(int(i.x + i.width), int(i.y + i.height)),
                         CV_RGB(0, 255, 0), 3, 8, 0)


def get_image():
    im = highgui.cvQueryFrame(camera)
    detect(im)
    return opencv.adaptors.Ipl2PIL(im)

fps = 30.0
pygame.init()
window = pygame.display.set_mode((640,480))
pygame.display.set_caption("WebCam Demo")
screen = pygame.display.get_surface()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT or event.type == KEYDOWN:
            sys.exit(0)

    im = get_image()
    pg_img = pygame.image.frombuffer(im.tostring(), im.size, im.mode)
    screen.blit(pg_img, (0,0))
    pygame.display.flip()
    pygame.time.delay(int(1000 * 1.0/fps))
