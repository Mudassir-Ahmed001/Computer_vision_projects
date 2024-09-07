import random
import time
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp


print("-->Press 's' to start the GAME")
print("-->Press 'q' to quit the GAME")


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)


timer = 0
state_result = False
start_game = False
score = [0, 0]



while True:
    imgBG = cv2.imread('BG.png')
    success, img = cap.read()



    img_scaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    img_scaled = img_scaled[:, 80:480]

    # Find hands
    hands, img = detector.findHands(img_scaled)

    if start_game == True:

        if state_result == False:
            timer = time.time() - initial_time
            cv2.putText(imgBG, str(int(timer)), (605,435), cv2.FONT_HERSHEY_PLAIN, 6, (255,0,255), 4)

            if timer>3:
                state_result=True
                timer = 0


                if hands:
                    player_move = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        player_move = 1
                    if fingers == [1,1,1,1,1]:
                        player_move = 2
                    if fingers == [0,1,1,0,0]:
                        player_move = 3


                    random_number = random.randint(1,3)

                    imgAI = cv2.imread(f'{random_number}.png', cv2.IMREAD_UNCHANGED)
                    cvzone.overlayPNG(imgBG, imgAI, (149,310))


                    #player Wins
                    if (player_move == 1 and random_number ==3) or \
                        (player_move == 2 and random_number == 1) or \
                        (player_move == 3 and random_number == 2):
                        score[1] += 1
                        print("_____________________________________________")
                        print("You Won")

                    # AI Wins
                    if (player_move == 3 and random_number == 1) or \
                        (player_move == 1 and random_number == 2) or \
                        (player_move == 2 and random_number == 3):
                        score[0] += 1
                        print("_____________________________________________")
                        print("AI Won, BETTER LUCK NEXT TIME")


    imgBG[234:654, 795:1195] = img_scaled


    if state_result:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(score[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(score[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    #cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    #cv2.imshow("scaled", img_scaled)



    key = cv2.waitKey(1)
    if key == ord('s'):
        start_game = True
        initial_time = time.time()
        state_result = False
    elif key == ord('q'):
        break