

#wrapper nad Netio knihovnou
#schova volani vice netii nad volani cisla zasuvek a nektere veci z netii

#netio smart power socket http://netio-products.com
#pip install Netio
#https://pypi.org/project/Netio/


#config
netio_json_url = 'http://10.10.134.11/netio.json'
netio_auth_user = 'netio'
netio_auth_passwd = 'netio'

#online demo vyrobce
#netio_json_url = 'http://powerdin-4pz.netio-products.com:22888/netio.json'
#etio_auth_user = 'write'
#netio_auth_passwd = 'demo'


##################
def ps_connect():
 from Netio import Netio
 print ("Connecting to Netio Power Socket, ...")
 #global netio1
 netio = Netio(netio_json_url, auth_rw=(netio_auth_user, netio_auth_passwd))
 #netio2 = Netio(netio2_json_url, auth_rw=(netio2_auth_user, netio2_auth_passwd))
 #netio3 = Netio(netio3_json_url, auth_rw=(netio3_auth_user, netio3_auth_passwd))
 print (" ok.")
 return(netio)

# how to use: prior to first operation with netio PS, use:
#import lmte-ps
#lmte-ps.ps_connect()

#def set_output(action):
#    netio1.set_output(1, action)
#    return()


# how to set PS output:
#  lmte_ps.set_output(OUTPUT_NUMBER, action)


# Outputs are numbered from 1 (in Netio)

#Output actions – “write” function
#• 0 – Turn OFF
#• 1 – Turn ON
#• 2 – Short OFF delay (restart)
#• 3 – Short ON delay
#• 4 – Toggle (invert the state)
#• 5 – No change
#• 6 – Ignored (return value from reading the tag)
#Current output value is in ”State” tag (0 / 1).


#def get_output(outputNumber):
#    if outputNumber == 1:
#        return(netio1.get_output(1))
#    return(0)

# how to read PS status and measurement:
#  lmte_ps.get_output(OUTPUT_NUMBER)   #print all measuring for this output
#  or just take Current value [mA]: ps.get_output(OUTPUT_NUMBER).Current)


#Output status – “read” function
#• 0 – Power OFF
#• 1 – Power ON


#Parameters for each power output:
# Variable Unit Description
# Current mA Instantaneous current for the specific power output
# TPF (True Power Factor) - Instantaneous True Power Factor for the specific power output
# Power W Instantaneous power (electrical load) for the specific power output.
# Energy Wh Instantaneous Energy counter value for the specific power output

#Parameters for the whole NETIO device:
# Variable Unit Description
# Voltage V Instantaneous voltage
# Frequency Hz Instantaneous frequency
# Total Current mA Instantaneous total current through all power outputs
# Overall True Power Factor - Instantaneous True Power Factor – weighted average from all meters
# Total power W Total Power of all power outputs (device’s own internal consumption is not included)
# Total Energy Wh Instantaneous value of the Total Energy counter
# Energy Start - Date and time of the last reset of all energy counters
