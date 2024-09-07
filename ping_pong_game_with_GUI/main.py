import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import mediapipe
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

#importing all images
img_bg = cv2.imread('Background.png')
img_gameover = cv2.imread('gameOver.png')
img_ball = cv2.imread('Ball.png', cv2.IMREAD_UNCHANGED)
bat_1 = cv2.imread('bat1.png', cv2.IMREAD_UNCHANGED)
bat_2 = cv2.imread('bat2.png', cv2.IMREAD_UNCHANGED)

#hand detector
detector = HandDetector(maxHands=2, detectionCon=0.8)

# variables
a = random.randint(100, 400)
b = random.randint(100, 500)
ball_position = [a, b]
speedX = 28
speedY = 28
game_over = False
score = [0, 0]


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgraw = img.copy()


    hands, img = detector.findHands(img, flipType=False)


    #overlaying the img
    img = cv2.addWeighted(img, 0.2, img_bg, 0.8, 0)



    # checking for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = bat_1.shape
            y1 = y - h1//2
            y1 = np.clip(y1, 20, 415)
            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, bat_1, (59, y1))
                if 59 < ball_position[0] < (59+w1) and y1 < ball_position[1] < (y1+h1):
                    speedX = -speedX
                    ball_position[0] += 30
                    score[0] += 1



            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, bat_2, (1195, y1))
                if 1195 - 50 < ball_position[0] < 1195-30 and y1 < ball_position[1] < (y1+h1):
                    speedX = -speedX
                    ball_position[0] -= 30
                    score[1] += 1


    #game over
    if ball_position[0]<0 or ball_position[0]>1200:
        game_over = True

    if game_over:
        img = img_gameover
        if score[0]>score[1]:
            cv2.putText(img, str(score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)
            cv2.putText(img, "player 1 WON", (300,650), cv2.FONT_HERSHEY_COMPLEX, 1.5, (200, 0, 200), 5)
        elif score[1]>score[0]:
            cv2.putText(img, str(score[1]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200, 0, 200), 5)
            cv2.putText(img, "player 2 WON", (900,650), cv2.FONT_HERSHEY_COMPLEX, 1.5, (200, 0, 200), 5)

    else:
        # ball moving
        if ball_position[1] >= 500 or ball_position[1] <= 10:
            speedY = -speedY

        ball_position[0] += speedX
        ball_position[1] += speedY
        img = cvzone.overlayPNG(img, img_ball, ball_position)

        cv2.putText(img, str(score[0]), (300,650), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255,255), 5)
        cv2.putText(img, str(score[1]), (900,650), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255,255), 5)



    #displaying the video below
    img[580:700, 20:233] = cv2.resize(imgraw, (213, 120))




    cv2.imshow("video", img)

    key = cv2.waitKey(1)
    if key == ord('r'):
        ball_position = [a, b]
        speedX = 28
        speedY = 28
        game_over = False
        score = [0, 0]
        img_gameover = cv2.imread('gameOver.png')
    elif key == ord('q'):
        break

