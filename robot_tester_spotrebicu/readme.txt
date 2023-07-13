Instalace na čistý počítač ------------------- (pouze poprvé)


Naistalovat python 3.x (ozkoušeno na 3.8) z MS Store (obsahuje instalátor PIP)

pip install Netio

pip install dynamixel-sdk

pip install pysimplegui 

nakopírovat python skripty:
	git clone https://github.com/lamasek/customer_fast.git
		lmte_gui.py
		lmte_ps.py
		lmte_servo_dynamixel_AX_12.py
		testScript_001.py

Nastavit IP adresu IP zásuvek Netio ve skriptu lmte_ps.py

Potřebujeme zjistit na jaký COM port je zapojeno U2D2 se servy, nejsnaší možnost:

Nainstalujeme Dynamixel Wizard
	https://www.robotis.com/


Spuštění ----------------------------------------------

Nainstalováno a nakopírováno do:
	C:\fast.cz-testerSpotrebicu> 

spuštění ovládacího GUI (z příkayové řádky)
	python lmte_gui.py

testy spouštíme
	python testScript_001.py


