import spidev
import time
import os
import RPi.GPIO as GPIO

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

spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 1000000

def ReadADC(ch):
    if (ch > 7) or (ch < 0):
        return -1
    adc = spi.xfer2([1, (8+ch)<<4, 0])
    data = ((adc[1]&3)<<8) + adc[2]
    return data

def ReadVolt(data, deci):
    volts = (data*3.3)/float(1023)
    volts = round(volts, deci)
    return volts

light_ch_1 = 0
light_ch_2 = 1
light_ch_3 = 6
light_ch_4 = 7


delay = 0.2

prev = 0

#change(1,12)
#time.sleep(1)
tree_flag = 0
tree_in = 0
tree_deltaT = 0
try: 
    while True:
        light_data_1 = ReadADC(light_ch_1)
        light_data_2 = ReadADC(light_ch_2)
        light_data_3 = ReadADC(light_ch_3)
        light_data_4 = ReadADC(light_ch_4)
        
        #light_volts_1 = ReadVolt(light_data_1,2)
        #light_volts_2 = ReadVolt(light_data_2,2)
        #light_volts_3 = ReadVolt(light_data_3,2)
        #light_volts_4 = ReadVolt(light_data_4,2)

        #print("Light : ", light_data_1 , " -> Volts : ", light_volts)
        print("Light 1~4 : {0} {1} {2} {3}".format(light_data_1, light_data_2, light_data_3, light_data_4))
        if ( light_data_2 <= 100):# & tree_flag == 0 ):
            #print("Tree is coming !!!")
            tree_in = time.time()
            tree_flag = 1
        if ( light_data_1 <= 100 ):
            tree_oops = time.time()
            tree_flag = 0
            tree_deltaT = tree_oops - tree_in
            print("Delta T : " , tree_deltaT)
            change(1, 3)
            change(2, 3)
            time.sleep(0.3)            
            change(1, 2)
            change(2, 2)
            #time.sleep(0.3)
        #else :
        #    change(1, 2)
        #    time.sleep(0.2)
        prev = light_data_1
        #change(1,2)
        #time.sleep(delay)
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
    GPIO.cleanup()
    spi.close()
    print("Done")
