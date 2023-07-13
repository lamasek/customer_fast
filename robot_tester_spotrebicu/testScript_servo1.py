

import time

import lmte_ps
ps = lmte_ps.ps_connect()

import lmte_servo_dynamixel_AX_12 as lmte_servo

SERVO_ID = 2    #ktere servo ovladame - 1 nebo 2

SERVO_OFF = 515
SERVO_ON = 600

lmte_servo.connect()
lmte_servo.torque_enable(SERVO_ID)
lmte_servo.go_to(SERVO_ID, SERVO_OFF)


ps.set_output(1, 1) # [zapne výstup 1 na zásuvce 1 - zapne zásuvku]


#definice funkce myexit() - spusti se v pripade jakehokoliv konce program - pretizeni, nezapnuti i normalniho ukonceni
# musi vypnout zasuvky a spotrebic
def myexit():
    ps.set_output(1, 0)
    lmte_servo.go_to(SERVO_ID, SERVO_OFF)
    time.sleep(3)
    lmte_servo.torque_disable(SERVO_ID)
    lmte_servo.disconnect()
    exit()



for i in range (1,5): # počet cyklů testu
    print("Cyklus " + str(i))

    #ZAPNUTO ----------------------------------------------------
    lmte_servo.go_to(SERVO_ID, SERVO_ON)
    time.sleep(3.5) #po zadani povelu servu je nutno pockat nez servo dojede a zapne spotrebic, pak pockame nez nabehne spotrebic a pak teprve muzeme merit normalni odber (čas po kterém začne měřit)

    ps_get_output = ps.get_output(1)
    ps_current = ps_get_output[5]
    print(" Zatizeni: " + str(ps_current) + "mA")

    if ps_current > 1200: #maximální limit proudu v mA
        print(" Stop pro pretizeni: " + str(ps_current) + "mA")
        myexit()

    if ps_current < 400: #minimální limit proudu v mA
        print(" Stop pro nezatizeni: " + str(ps_current) + "mA")
        myexit()

    time.sleep(5) #doba provozu zařízení poté co proběhne měření

    #VYPNUTO ----------------------------------------------------
    lmte_servo.go_to(SERVO_ID, SERVO_OFF)
    time.sleep(4) #po zadani povelu servu je nutno pockat nez servo dojede a vypne spotrebic, pak pockame nez dobehne spotrebic a pak teprve muzeme merit odber ve vypnutem stavu

    ps_get_output = ps.get_output(1)
    ps_current = ps_get_output[5]
    print(" Zatizeni vypnuto: " + str(ps_current) + "mA")
    if ps_current > 100: # přetížení ve vypnutém stavu
        print(" Stop pro pretizeni ve vypnutem stavu: " + str(ps_current) + "mA")
        myexit()

    time.sleep(2) # zbytek cekani ve stavu vypnuteho spotrebice


#normalni konec po dokonceni vsech cyklu
myexit()
