# ampy -p COM10 get boot.py
from ntptime import settime
D0 = const(16)
D1 = const(5)
D2 = const(4)  
D3 = const(0)
D4 = const(2) # Internal LED
D5 = const(14)
D6 = const(12)
D7 = const(13)
D8 = const(15) # 10K pull Down

def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Yelwor', '**********')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
def no_debug():
    import esp
    # this can be run from the REPL as well
    esp.osdebug(None)
	
import gc
#import webrepl
from upysh import *	
no_debug()
connect()
settime()
#webrepl.start()
gc.collect()