import cv2 
from detector import BlobDetector
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT) # for servo 1
GPIO.setup(12,GPIO.OUT) # for servo 2
servo_1 = GPIO.PWM(11,50)
servo_2 = GPIO.PWM(12,50)

servo_1.start(0)
servo_2.start(0)

def change(index, duty):
    # servo_1.ChangeDutyCycle(duty)
    if index == 1:
        servo_1.ChangeDutyCycle(duty)
    elif index == 2:
        servo_2.ChangeDutyCycle(duty)


cap = cv2.VideoCapture(0)
try:
    while True:
        ret, frame = cap.read()
        if ret == True:
            detector = BlobDetector(frame)
            keypoints = detector.detect_keypoint(frame)
            
            for kp in keypoints:
                tree_x = kp.pt[0]
                # should be adjusted according to camera situation
                if tree_x < 450 and tree_x > 329:
                    print('jump', tree_x)
                    change(1,9)
                    time.sleep(0.08)
                    change(1,2)
                    break
       
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

except KeyboardInterrupt:
    pass

finally:
    change(1, 2)
    change(2, 2)
    time.sleep(0.5)
    change(1, 0)
    change(2, 0)
    servo_1.stop()
    servo_2.stop()
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()

