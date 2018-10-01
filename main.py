'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
'''
import pygame
import cv2
import subprocess
import sys
import numpy as np
import copy
import math

from pygame.locals import *

from label_image import *

## GitHub Izane: Project: Fingers-Detection-using-OpenCV-and-Python
## link: https://github.com/lzane/Fingers-Detection-using-OpenCV-and-Python
# parameters
cap_region_x_begin = 0.5  # start point/total width
cap_region_y_end = 0.8  # start point/total width
threshold = 60  # BINARY threshold
bgSubThreshold = 50

# variables
isBgCaptured = 0  # bool, whether the background captured


def printThreshold(thr):
    print("! Changed threshold to " + str(thr))


# Camera
camera = cv2.VideoCapture(0)
camera.set(10, 200)
cv2.namedWindow('trackbar')
cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)


## end cite code

class PygameGame(object):
    def init(self):
        self.mode = "main"
        self.titleFont = pygame.font.SysFont("Avenir", 50)
        self.normFont = pygame.font.SysFont("Avenir", 30)
        self.imgCount = -1
        self.captured = False
        self.calculated = "0"

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier): \
        self._keys[keyCode] = True

    def keyReleased(self, keyCode, modifier):
        self._keys[keyCode] = False

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        # title text
        titleText = self.titleFont.render('A S L     I n t e r p r e t e r', 1, (0, 0, 0))
        titleRect = titleText.get_rect(center=(self.width // 2, self.height // 8))
        screen.blit(titleText, titleRect)

        if self.captured:
            captureText = self.normFont.render('Captured Image', 1, (0, 0, 0))
            captureRect = captureText.get_rect(center=(self.width * 13 // 18, self.height // 3 - 30))
            screen.blit(captureText, captureRect)
            screen.blit(pygame.transform.scale(pygame.image.load("images/test.png").convert(),
                                               (self.width // 3, self.width // 3)),
                        (self.width * 5 // 9, self.height // 3))
            exampleText = self.normFont.render('Example Sign: %s' % self.calculated, 1, (0, 0, 0))
            exampleRect = exampleText.get_rect(center=(self.width * 5 // 18, self.height // 3 - 30))
            screen.blit(exampleText, exampleRect)
            screen.blit(pygame.transform.scale(pygame.image.load("images/%s.jpg" % self.calculated).convert(),
                                               (self.width // 3, self.width // 3)), (self.width // 9, self.height // 3))

    # capture

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=800, height=600, fps=50, title="ASL Interpreter"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):
        clock = pygame.time.Clock()
        flags = DOUBLEBUF
        screen = pygame.display.set_mode((self.width, self.height), flags)
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        print("Game Start")
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*event.pos)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*event.pos)
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)

            # capture code cite
            if camera.isOpened():
                ret, frame = camera.read()
                frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
                # frame = cv2.flip(frame, 1)  # flip the frame horizontally
                cv2.rectangle(frame, (0, 0),
                              (int(frame.shape[1] * 0.5), int(frame.shape[0] * 0.8)), (255, 255, 255), 2)
                # cv2.imshow('original', frame)

                #  Main operation
                img = frame[0:int(frame.shape[0] * 0.8), 0:int(frame.shape[1] * 0.5)]  # clip the ROI
                cv2.imshow('hand', img)

                # Keyboard OP
                k = cv2.waitKey(10)
                if k == 27:  # press ESC to exit
                    break
                elif k == 99:  # c to capture
                    self.captured = True
                    self.imgCount += 1
                    # cv2.imwrite('images/image%d.png' % self.imgCount, img)
                    cv2.imwrite('images/test.png', img)
                    print('Captured Image!')
                    proc = subprocess.Popen(['./run.sh'], shell=True)
                    f = open("info.txt", "r")
                    largest = 0
                    currC = ""
                    currN = 0
                    for line in f:
                        x = 0
                        while x <= 1:
                            if x == 0:
                                currC = line[x]
                                print(currC)
                            else:
                                currN = float(line[x:])
                                print(currN)
                            x += 1
                        if(currN > largest):
                            largest = currN
                            self.calculated = currC
                    self.redrawAll(screen)
                    print(largest)
                    print("test")
            # end of capture code
            pygame.display.flip()

        print("Window Closed!")
        pygame.quit()


def main():
    game = PygameGame()
    game.run()


if __name__ == '__main__':
    main()
