from time import sleep
from machine import RTC
import ntptime
try:
    ntptime.settime()
except Exception as e:
    print(e)

modetoint = {"auto":65, "cool":66, "heat":67, "dry":68, "fan_only":69}
inttomode = dict(map(reversed, modetoint.items()))

fanmodetoint = {"quiet":49, "lvl_1": 50, "lvl_2":51, "lvl_3":52, "lvl_4":53, "lvl_5":54, "auto":65} 
inttofanmode = dict(map(reversed, fanmodetoint.items()))

swingtoint = {"off": 49, "on":65, "on-h":66, "on-vh":67}
inttoswing = dict(map(reversed, swingtoint.items()))

statetoint = {"on":48, "off":49}
inttostate = dict(map(reversed, statetoint.items()))

def checksum(msg,function):
    numb = 434 - msg - function
    if numb > 256:
        retval = numb - 256
    else:
        retval = numb
    return retval


def logprint(msg):
    rtc = RTC()
    t = rtc.datetime()
    #(2020, 4, 22, 2, 8, 43, 38, 88387)
    # yyyy, m, dd, ?, h, mm, ss, ms
    timestamp = str(t[2]) + "-" + str(t[1]) + "-" + str(t[0]) + " " + str(t[4]) + ":" + str(t[5]) + ":" + str(t[6]) + "." + str(t[7])
    result = str(timestamp) + " -> " + str(msg)
    print(result)
 


def swingControl(msg):
    function_code = 163
    message = msg.decode("utf-8")
    
    try:
        function_value = swingtoint[message]
        control_code = checksum(function_value,function_code)
        mylist = (2,0,3,16,0,0,7,1,48,1,0,2,function_code,function_value,control_code)
        getlist = (2,0,3,16,0,0,6,1,48,1,0,1,function_code,17)
        myvalues = (mylist, getlist)
    except Exception as e:
        myvalues = False
    return myvalues

def modeControl(msg):
    function_code = 176
    message = msg.decode("utf-8")
    try:
        function_value = modetoint[message]
        control_code = checksum(function_value,function_code)
        mylist = (2,0,3,16,0,0,7,1,48,1,0,2,function_code,function_value,control_code)
        getlist = (2,0,3,16,0,0,6,1,48,1,0,1,function_code,4)
        myvalues = (mylist, getlist)
    except Exception as e:
        myvalues = False
    return myvalues

def fanControl(msg):
    function_code = 160
    message = msg.decode("utf-8")
    try:
        function_value = fanmodetoint[message]
        control_code = checksum(function_value,function_code)
        mylist = (2,0,3,16,0,0,7,1,48,1,0,2,function_code,function_value,control_code)
        getlist = (2,0,3,16,0,0,6,1,48,1,0,1,function_code,20)
        myvalues = (mylist, getlist)
    except Exception as e:
        myvalues = False
    return myvalues



def stateControl(msg):
    function_code = 128
    message = msg.decode("utf-8")
    try:
        function_value = statetoint[message]
        control_code = checksum(function_value,function_code)
        mylist = (2,0,3,16,0,0,7,1,48,1,0,2,function_code,function_value,control_code)
        getlist = (2,0,3,16,0,0,6,1,48,1,0,1,function_code,52)
        myvalues = (mylist, getlist)
    except Exception as e:
        myvalues = False
    return myvalues

def setpointVal(msg):
    function_code = 179
    try:
        function_value = int(msg)
        control_code = checksum(function_value,function_code)
        mylist = (2,0,3,16,0,0,7,1,48,1,0,2,function_code,function_value,control_code)
        getlist = (2,0,3,16,0,0,6,1,48,1,0,1,function_code,1)
        myvalues = (mylist, getlist)
    except Exception as e:
        myvalues = False
    return myvalues

     
def queryall():
     bootlist = []
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,128,52))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,176,4))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,179,1))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,160,20))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,135,45))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,163,17))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,187,249))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,190,246))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,203,233))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,136,44))
     #bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,134,46))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,144,36))
     bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,148,32))
     return bootlist    


def watchdog():
    bootlist = []
    bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,187,249))
    bootlist.append((2,0,3,16,0,0,6,1,48,1,0,1,190,246))
    return bootlist



