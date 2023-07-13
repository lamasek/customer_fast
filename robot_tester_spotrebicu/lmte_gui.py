#!python3


# python -m pip install pysimplegui
import PySimpleGUI as sg

import lmte_ps
ps = lmte_ps.ps_connect()

#  ps.set_output(OUTPUT_NUMBER, action)
#  ps.get_output(OUTPUT_NUMBER)   #print all measuring for this output


import lmte_servo_dynamixel_AX_12 as lmte_servo
lmte_servo.connect()


servo1_goal_position = 512
servo2_goal_position = 512

servo_mouse_wheel_steps = 1

#lmte_servo.set_torque_limit(DXL_ID, 10)

#parsing arguments
#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument("ps", help="Power Supply control")
#parser.add_argument("ps_num", type=int, help="PS Outlet - 1..3")
#parser.add_argument("ps_action", choices=['on', 'off', 'status', 'getCurrent'])

#args = parser.parse_args()

#main code

sg.theme('DarkTeal6')   # Add a touch of color
# All the stuff inside your window.
layout = [
            [ sg.Text('Power Supply -------------------------') ],
            [ sg.Text('  Output 1: '), sg.Text('State:'), sg.Text('???', key="ps-o1-state"), sg.Text('Turn it:'), sg.Button('On', key="ps-o1-on"), sg.Button('Off', key="ps-o1-off"), sg.Text("Current taken: ???????? [mA]", key="ps-o1-current") ],
            #[ sg.Text('  Output 2: '), sg.Text('State:'), sg.Text('???', key="ps-o2-state"), sg.Text('Turn it:'), sg.Button('On', key="ps-o2-on"), sg.Button('Off', key="ps-o2-off"), sg.Text("Current taken: ???????? [mA]", key="ps-o2-current") ],
            #[ sg.Text('  Output 3: '), sg.Text('State:'), sg.Text('???', key="ps-o3-state"), sg.Text('Turn it:'), sg.Button('On', key="ps-o3-on"), sg.Button('Off', key="ps-o3-off"), sg.Text("Current taken: ???????? [mA]", key="ps-o3-current") ],
            [ sg.Text('Servos -------------------------------') ],
            [   sg.Text('  1: '),
                #sg.Checkbox('', default=False, change_submits = True, key="servo1-checkbox"),
                sg.Text(' Torque Enable:'),sg.Checkbox('', default=False, change_submits = True, key="servo1-torque_enable"),
                sg.Text(' Position: Goal:'), sg.Slider(range=(0,1023), default_value=512, size=(10,15), orientation='horizontal', font=('Helvetica', 10), key="servo1-goal-position"),
                sg.Text(' Current:'), sg.Slider(range=(0,1023), default_value=512, size=(10,15), orientation='horizontal', font=('Helvetica', 10), key="servo1-current-position"),
                sg.Text(' Turn it:'), sg.Button('-10', key="servo1-go--10"),
                sg.Button('-1', key="servo1-go--1"), sg.Button('middle ', key="servo1-middle"),
                sg.Button('+1', key="servo1-go-+1"), sg.Button('+10', key="servo1-go-+10"),
                sg.Text(' Present load: ???? [step]', key="servo1-present-load"),
            ],
            [   sg.Text('  2: '),
                #sg.Checkbox('', default=False, change_submits = True, key="servo2-checkbox"),
                sg.Text(' Torque Enable:'),sg.Checkbox('', default=False, change_submits = True, key="servo2-torque_enable"),
                sg.Text(' Position: Goal:'), sg.Slider(range=(0,1023), default_value=512, size=(10,15), orientation='horizontal', font=('Helvetica', 10), key="servo2-goal-position"),
                sg.Text(' Current:'), sg.Slider(range=(0,1023), default_value=512, size=(10,15), orientation='horizontal', font=('Helvetica', 10), key="servo2-current-position"),
                sg.Text(' Turn it:'), sg.Button('-10', key="servo2-go--10"),
                sg.Button('-1', key="servo2-go--1"), sg.Button('middle ', key="servo2-middle"),
                sg.Button('+1', key="servo2-go-+1"), sg.Button('+10', key="servo2-go-+10"),
                sg.Text(' Present load: ???? [step]', key="servo2-present-load"),
            ],
#            [ sg.Text('Temperature sensors -----------------') ],
#            [ sg.Text('  1: '), sg.Text('Temperature:'), sg.Text('??? [C]', key="temp1-temp"), ],
#            [ sg.Text('Settings -----------------') ],
#            [ sg.Text(" Mouse wheel step makes servo steps:"), sg.Spin([i for i in range(1,100)], initial_value=1, key="servo-mouse-wheel-steps") ],
            [ sg.Button('Exit') ]
        ]

# Create the Window
window = sg.Window('LMTE - quick access and control window', layout, return_keyboard_events=True)
# Event Loop to process "events" and get the "values" of the inputs

while True:             # Event Loop
    event, values = window.read(timeout = 1000) # i kdyz neprijde od uzivatele zadna interakce, tak po timeout [ms] vyskoci z read
    print (" Loop ---------------------")
    #servo_mouse_wheel_steps = values["servo-mouse-wheel-steps"]

    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks Exit
        break
    ################## PS ####################
    elif event == "ps-o1-on":
        print ("PS - Output1 - turning On ..., ")
        ps.set_output(1, 1)
        print ("   ok.")
    elif event == "ps-o1-off":
        print ("PS - Output1 - turning Off ..., ")
        ps.set_output(1, 0)
        print ("   ok.")
#    elif event == "ps-o2-on":
#        print ("PS - Output2 - turning On ..., ")
#        set_output(2, 1)
#        print ("   ok.")
#    elif event == "ps-o2-off":
#        print ("PS - Output2 - turning Off ..., ")
#        lmte_ps.set_output(2, 0)
#        print ("   ok.")
#    elif event == "ps-o3-on":
#        print ("PS - Output3 - turning On ..., ")
#        lmte_ps.set_output(3, 1)
#        print ("   ok.")
#    elif event == "ps-o3-off":
#        print ("PS - Output3 - turning Off ..., ")
#        lmte_ps.set_output(3, 0)
#        print ("   ok.")
    ################## SERVO1 ####################
    elif event == "servo1-torque_enable":
        if values['servo1-torque_enable'] == True:
            print ("Servo 1 Torque enable..., ")
            lmte_servo.torque_enable(1)
        else:
            print ("Servo 1 Torque disable..., ")
            lmte_servo.torque_disable(1)
    elif event == "servo1-go--10":
        print ("Servo 1 going 10 step left ..., ")
        servo1_goal_position = servo1_goal_position -10
        lmte_servo.go_to(1,servo1_goal_position)
    elif event == "servo1-go--1":
        print ("Servo 1 going 1 step left ..., ")
        servo1_goal_position = servo1_goal_position -1
        lmte_servo.go_to(1,servo1_goal_position)
    elif event == "servo1-middle":
        print ("Servo 1 going to middle = 150dg ..., ")
        servo1_goal_position = 512
        lmte_servo.go_to(1,servo1_goal_position)
    elif event == "servo1-go-+1":
        print ("Servo 1 going 1 step right ..., ")
        servo1_goal_position = servo1_goal_position +1
        lmte_servo.go_to(1,servo1_goal_position)
    elif event == "servo1-go-+10":
        print ("Servo 1 going 10 step right ..., ")
        servo1_goal_position = servo1_goal_position +10
        lmte_servo.go_to(1,servo1_goal_position)
    ################## SERVO2 ####################
    elif event == "servo2-torque_enable":
        if values['servo2-torque_enable'] == True:
            print ("Servo 2 Torque enable..., ")
            lmte_servo.torque_enable(2)
        else:
            print ("Servo 2 Torque disable..., ")
            lmte_servo.torque_disable(2)
    elif event == "servo2-go--10":
        print ("Servo 2 going 10 step left ..., ")
        servo2_goal_position = servo2_goal_position -10
        lmte_servo.go_to(2,servo2_goal_position)
    elif event == "servo2-go--1":
        print ("Servo 2 going 1 step left ..., ")
        servo2_goal_position = servo2_goal_position -1
        lmte_servo.go_to(2,servo2_goal_position)
    elif event == "servo2-middle":
        print ("Servo 2 going to middle = 150dg ..., ")
        servo2_goal_position = 512
        lmte_servo.go_to(2,servo1_goal_position)
    elif event == "servo2-go-+1":
        print ("Servo 2 going 1 step right ..., ")
        servo2_goal_position = servo2_goal_position +1
        lmte_servo.go_to(2,servo2_goal_position)
    elif event == "servo2-go-+10":
        print ("Servo 2 going 10 step right ..., ")
        servo2_goal_position = servo2_goal_position +10
        lmte_servo.go_to(2,servo2_goal_position)
#    ################## MOUSE WHEEL ####################
#    elif event == "MouseWheel:Down":
#        if values['servo1-checkbox'] == True:
#            servo1_goal_position = servo1_goal_position -1*servo_mouse_wheel_steps
#            lmte_servo.go_to(1,servo1_goal_position)
#        if values['servo2-checkbox'] == True:
#            servo2_goal_position = servo2_goal_position -1*servo_mouse_wheel_steps
#            lmte_servo.go_to(2,servo2_goal_position)
#    elif event == "MouseWheel:Up":
#        if values['servo1-checkbox'] == True:
#            servo1_goal_position = servo1_goal_position +1*servo_mouse_wheel_steps
#            lmte_servo.go_to(1,servo1_goal_position)
#        if values['servo2-checkbox'] == True:
#            servo2_goal_position = servo2_goal_position +2*servo_mouse_wheel_steps
#            lmte_servo.go_to(2,servo2_goal_position)
    ################## ELSE ####################
    elif event == "__TIMEOUT__":
        a=1
    else:
        print("Unhandled event, event: " + event)
        print(" values: ")
        print(values)
    #PS
    ps1_get_output = ps.get_output(1)
    #print (ps1_get_output)
    #print (ps1_get_output[4])
    #neumim vybrat hodnoty z tuple pomoci klice, hodnoty jsou Output(ID=1, Name='Power output 1', State=1, Action=<ACTION.IGNORED: 6>, Delay=2020, Current=57, PowerFactor=0.0, Load=0, Energy=371)
    # kde ID je index 0, Name je index 1, ...

    window['ps-o1-state'].update(ps1_get_output[1])
    window['ps-o1-current'].update("Current taken: {:>10}  [mA]".format(ps1_get_output[5]))

#    window['ps-o2-state'].update(ps.get_output(2).State)
#    window['ps-o2-current'].update("Current taken: {:>10}  [mA]".format(ps.get_output(2).Current))

#    window['ps-o3-state'].update(ps.get_output(3).State)
#    window['ps-o3-current'].update("Current taken: {:>10}  [mA]".format(ps.get_output(3).Current))

    #servo
    #window['servo1-state'].update()
    window['servo1-goal-position'].update(servo1_goal_position)
    window['servo1-current-position'].update(lmte_servo.get_current_position(1))
    window['servo1-present-load'].update("Present load: {:4}  [%]".format(lmte_servo.get_present_load(1)))
    window['servo2-goal-position'].update(servo2_goal_position)
    window['servo2-current-position'].update(lmte_servo.get_current_position(2))
    window['servo2-present-load'].update("Present load: {:4}  [%]".format(lmte_servo.get_present_load(2)))

lmte_servo.disconnect()

window.close()
