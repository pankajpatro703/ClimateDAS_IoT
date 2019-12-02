from boltiot import Bolt
import conf,time
mybolt=Bolt(conf.API_KEY,conf.DEVICE_ID)
resp=mybolt.serialBegin(9600)
time.sleep(10)
mybolt.serialWrite("1 2 3 \n")
time.sleep(10)
