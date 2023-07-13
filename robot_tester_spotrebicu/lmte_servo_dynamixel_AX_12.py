

from dynamixel_sdk import *                    # Uses Dynamixel SDK library


# Control table address - pro kazde servo muze byt jine tohle je pro AX-12A
ADDR_MX_TORQUE_ENABLE      = 24
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_TORQUE_LIMIT       = 34
ADDR_MX_PRESENT_POSITION   = 36
ADDR_MX_PRESENT_LOAD       = 40


# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel
#DXL_ID  je predelan jako parametr funkce

# Default setting
#DXL_ID                      = 1                 # Dynamixel ID : 1
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = 'COM10'    # Check which port is being used on your controller

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

#GOAL_POSITION
#0 ~ 1,023 (0x3FF) is available. The unit is 0.29°
#0 ~ #))dg, prostredek je 512=150dg



# how to use: prior to first operation with servo, use:
#import lmte-servo
#lmte_servo.connect()




def connect():
    #from Netio import Netio
    print ("lmte-servo: " + "Connecting to Servo, ...")

    global portHandler
    global packetHandler

    portHandler = PortHandler(DEVICENAME)
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    if portHandler.openPort():
        print("lmte-servo: " + "Succeeded to open the port")
    else:
        print("lmte-servo: " + "Failed to open the port")
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        print("Press any key to terminate...")
        getch()
        quit()


def disconnect():
    # Close port
    portHandler.closePort()




def torque_enable(DXL_ID):
    # Enable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")
    #return(ps)





def torque_disable(DXL_ID):
    # Disable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))






def go_to(DXL_ID, angle):
    print ("lmte-servo: going  to " + str(angle) + " dg.")

    # Write goal position
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_MX_GOAL_POSITION, angle)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    # return(0)


def get_current_position(DXL_ID):
    # Read present position
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_MX_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        quit
    print("lmte-servo: " + "Current position: "+str(dxl_present_position))
    #workaround
    if dxl_present_position > 1023:
         return(-1)
    return(dxl_present_position)

def get_present_load(DXL_ID):
    # Read present position
    dxl_present_load, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_MX_PRESENT_LOAD)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
        quit
    print("lmte-servo: " + "Present load (0-2048): "+str(dxl_present_load))
    #workaround
    dxl_present_load_percent = (dxl_present_load - 1024)/10.24
    return(dxl_present_load_percent)



#Torque Limit (34)
#It is the value of the maximum torque limit. 0 ~ 1,023(0x3FF) is available, and the unit is about 0.1%. For example, if the value is 512, it is about 50%; that means only 50% of the maximum torque will be used. If the power is turned on, the value of Max Torque(14) is used as the initial value.
def set_torque_limit(DXL_ID, torque_percents):

    torque = int(torque_percents*10.23)
    print ("lmte-servo: Setting torque limit to " + str(torque))

    # Write goal position
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_MX_TORQUE_LIMIT, torque)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    # return(0)
