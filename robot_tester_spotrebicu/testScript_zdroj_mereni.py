

import time

import lmte_ps
ps = lmte_ps.ps_connect()




#definice funkce myexit() - spusti se v pripade jakehokoliv konce program - pretizeni, nezapnuti i normalniho ukonceni
# musi vypnout zasuvky a spotrebic
def myexit():
    ps.set_output(1, 0)
    exit()


ps.set_output(1, 1) # [zapne výstup 1 na zásuvce 1 - zapne zásuvku]

for i in range (1,1000000000): # počet cyklů testu
    time.sleep(1)
    ps_get_output = ps.get_output(1)
    ps_current = ps_get_output[5]
    print("Cyklus " + str(i) + "; " + str(ps_current))

#normalni konec po dokonceni vsech cyklu
myexit()
