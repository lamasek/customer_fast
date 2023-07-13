


######## HEADERY
import time
import signal

import lmte_ps
ps = lmte_ps.ps_connect()

import lmte_servo_dynamixel_AX_12 as lmte_servo
#########################


# NASTAVENI parametru testu
SERVO_ID = 2    #ktere servo ovladame - 1 nebo 2
SERVO_OFF = 187
SERVO_ON = 789


##### START 
lmte_servo.connect() # připojíme se k servu
lmte_servo.torque_enable(SERVO_ID) # zapneme servo
lmte_servo.go_to(SERVO_ID, SERVO_OFF)


ps.set_output(1, 1) # [zapne výstup 1 na zásuvce 1 - zapne zásuvku]
time.sleep(4) # 

################ EXIT funkce - co se spustí po preruseni testů v případě chyby a stisknuti CTRL-C
# musi vypnout zasuvky a spotrebic
def myexit():
    print('Exit')
    ps.set_output(1, 0) #okamzite vypneme zasuvku
    lmte_servo.go_to(SERVO_ID, SERVO_OFF) # vypneme spotrebic
    time.sleep(3)
    lmte_servo.torque_disable(SERVO_ID) #vypneme servo
    lmte_servo.disconnect()
    exit()

def myexit_handler(signum, frame):
    myexit()

#myexit zavolame i v pripade stisknuti CTRL-C
signal.signal(signal.SIGINT, myexit_handler)

############# 



for i in range (1,100): # počet cyklů testu
    print("Cyklus " + str(i))

    #ZAPNUTO ----------------------------------------------------
    lmte_servo.go_to(SERVO_ID, SERVO_ON)
    time.sleep(6) # [s] po zadani povelu servu je nutno pockat nez servo dojede a zapne spotrebic, pak pockame nez nabehne spotrebic a pak teprve muzeme merit normalni odber (čas po kterém začne měřit)

    ps_get_output = ps.get_output(1)
    ps_current = ps_get_output[5]
    print(" Zatizeni: " + str(ps_current) + "mA")

    if ps_current > 2000: # [mA]
        print(" Stop pro pretizeni: " + str(ps_current) + "mA")
        myexit()

    if ps_current < 400:
        print(" Stop pro nezatizeni: " + str(ps_current) + "mA")
        myexit()

    time.sleep(120) # [s] doba provozu zařízení poté co proběhne měření

    #VYPNUTO ----------------------------------------------------
    lmte_servo.go_to(SERVO_ID, SERVO_OFF)
    time.sleep(4) #po zadani povelu servu je nutno pockat nez servo dojede a vypne spotrebic, pak pockame nez dobehne spotrebic a pak teprve muzeme merit odber ve vypnutem stavu

    ps_get_output = ps.get_output(1)
    ps_current = ps_get_output[5]
    print(" Zatizeni vypnuto: " + str(ps_current) + "mA")
    if ps_current > 100: # přetížení ve vypnutém stavu
        print(" Stop pro pretizeni ve vypnutem stavu: " + str(ps_current) + "mA")
        myexit()

    time.sleep(180) # zbytek cekani ve stavu vypnuteho spotrebice




