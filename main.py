import math
import random
import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1080)
cap.set(4, 1920)

detector = HandDetector(maxHands=1, detectionCon=0.8)


class SnakeGame:
    def __init__(self, path_food):
        self.points = [] #list of all points of snake
        self.lengths = [] #list of distances btw each point
        self.currentLength = 0 # total length of the snake
        self.allowedLength = 150 #total allowed length
        self.previousHead = 0, 0 # previous head point

        path_food = cv2.imread(path_food, cv2.IMREAD_UNCHANGED)
        path_food = cv2.resize(path_food, (75, 75), fx= 0.2, fy=0.2)
        self.imgFood = path_food
        self.hfood, self.wfood, _ = self.imgFood.shape
        food_points = 0, 0
        self.random_food_location()
        self.score = 0
        self.game_over = False

    def random_food_location(self):
        self.food_points = random.randint(100,1000), random.randint(100,600)

    def update(self, imgMain, currentHead):

        if self.game_over:
            cvzone.putTextRect(imgMain, "Game Over", [300,400], scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score is :-  {self.score}', [300, 550], scale=7, thickness=5, offset=20)
        else:


            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx-px, cy-py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy


            #length reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)

                    if self.currentLength < self.allowedLength:
                        break

            #checking if snake ate the food
            rx, ry = self.food_points
            if (rx - self.wfood//2) < cx < (rx + self.wfood//2) and (ry - self.hfood//2) < cy < (ry + self.hfood//2):
                self.random_food_location()
                self.allowedLength += 50
                self.score += 1


            #drawing snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i-1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[i-1], 20, (200, 0, 200,), cv2.FILLED)


            #drawing food
            rx, ry = self.food_points
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood, (rx-self.wfood//2, ry- self.hfood//2))
            cvzone.putTextRect(imgMain, f'Your Score is :-  {self.score}', [50, 80], scale=7, thickness=5, offset=10)



            # checking for collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            #cv2.polylines(imgMain, [pts], False, (0, 200, 0), 3)
            minimum_distance = cv2.pointPolygonTest(pts, (cx, cy), True)

            #print(minimum_distance)

            if -1 <= minimum_distance <= 1:
                print("hit")
                self.game_over = True
                self.points = []  # list of all points of snake
                self.lengths = []  # list of distances btw each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed length
                self.previousHead = 0, 0  # previous head point
                self.random_food_location()



        return imgMain


game = SnakeGame('Donut.png')

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False, draw=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2] #the reason why we are writing [0:2] is, if we do not mention it then it gives us 3 dimensions(x,y,z) but we only want  x,y
        img = game.update(img, pointIndex)


    cv2.imshow("img", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.game_over = False
        game.score = 0
    elif key == ord('q'):
        break