#uvozimo knjižnico za delo GPIO pini
from RPi import GPIO
 

 
step = 1 #shranimo korak, ki ga prištejemo ali odštejemo, ko se zavrti enkoder
paused = False #spremljamo stanje, kdaj se ustavimo
 
#Povemo kako bomo nastavljali GPIO pine; uporabimo logični način, to kar je zapisano na GPIO členu
GPIO.setmode(GPIO.BCM) 
 
#clk in dt sta spremenljivki, ki povesta kam bomo povezali pina enkoderja (S1, S2)
#sw e spremenljivka, ki pove kam je povezana tipka (key)
clk = 17
dt = 18
sw = 27
 
#set up the GPIO events on those pins
#GPIO.setup(pin, vhod/izhod, način)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
#Preveri in nastavi prvotno stanje
counter = 0 #števec, začnemo šteti z 0
clkLastState = GPIO.input(clk) #preberemo stanje ma pinu 17 - S2
dtLastState = GPIO.input(dt) #preberemo stanje ma pinu 18 - S1
swLastState = GPIO.input(sw) #preberemo stanje ma pinu 27 - KEY
 
#define functions which will be triggered on pin state changes
def clkClicked(channel):
        global counter #uporabimo globalno spremenljivko counter
        global step #uporabimo globalno spremenljivko step
 
        clkState = GPIO.input(clk) #preberemo stanje ma pinu 17 - S2
        dtState = GPIO.input(dt) #preberemo stanje ma pinu 18 - S1
 
        #Premikamo se v smeri urnega kazalca, če je pin 17 == 0 in pin 18 == 1
        if clkState == 0 and dtState == 1:
                #prištejemo korak - vrtimo se v smeri urinega kazalca
                counter = counter + step
                print ("Counter ", counter)
 
def dtClicked(channel):
        global counter
        global step
 
        clkState = GPIO.input(clk) #preberemo stanje ma pinu 17 - S2
        dtState = GPIO.input(dt) #preberemo stanje ma pinu 18 - S1
         
         #Premikamo se v smeri urnega kazalca, če je pin 17 == 1 in pin 18 == 0
        if clkState == 1 and dtState == 0:
                #prištejemo korak - vrtimo se v nasprotni smeri urinega kazalca
                counter = counter - step
                print ("Counter ", counter)
 
def swClicked(channel):
        global paused #povemo, da bomo uporabili globalno spremenljivko
        paused = not paused #obrnemo vrednost spremeljivke paused
        print ("Paused ", paused)             
                 
#na začetku sprintamo začetna stanja
print ("Initial clk:", clkLastState)
print ("Initial dt:", dtLastState)
print ("Initial sw:", swLastState)
print ("=========================================")
 
#nastavimo prekinitve
#GPIO.add_event_detect(pin, kdaj preberemo FALLING/RISING/*ONCHANGE*, katero funkcijo želimo poklicati, nastavimo koliko časa naj prekinitev počaka pred ponovno izvedbo)
GPIO.add_event_detect(clk, GPIO.FALLING, callback=clkClicked, bouncetime=300)
GPIO.add_event_detect(dt, GPIO.FALLING, callback=dtClicked, bouncetime=300)
GPIO.add_event_detect(sw, GPIO.FALLING, callback=swClicked, bouncetime=300)
 
input("Start monitoring input")
 
#počistimo nastavitve vseh pinov
GPIO.cleanup()