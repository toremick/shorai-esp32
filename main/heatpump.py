from main import hpfuncs
from main.ota_updater import OTAUpdater
from machine import UART

global uart
uart = UART(1, 9600)
uart.init(9600,bits = 8,parity = 0,stop = 1,rx = 32,tx = 33,timeout = 10, timeout_char=50)
import uasyncio as asyncio
from main.mqtt_as import MQTTClient
from config import config
import time
from time import sleep
import machine
power_state = 'OFF'



#topic_prefix = "heatpump"
#mqtt_server = '192.168.2.30'
#client_id ='hpesp32-1'

topic_sub_setp =  b"" + config['maintopic'] + "/setpoint/set"
topic_sub_state =  b"" + config['maintopic'] + "/state/set"
topic_sub_fanmode =  b"" + config['maintopic'] + "/fanmode/set"
topic_sub_swingmode =  b"" + config['maintopic'] + "/swingmode/set"
topic_sub_mode =   b"" + config['maintopic'] + "/mode/set"
topic_sub_doinit =  b"" + config['maintopic'] + "/doinit"
topic_sub_restart =  b"" + config['maintopic'] + "/restart"
topic_sub_watchdog =  b"" + config['maintopic'] + "/watchdog"
topics = [topic_sub_setp, topic_sub_state, topic_sub_doinit, topic_sub_fanmode, topic_sub_mode, topic_sub_swingmode, topic_sub_restart, topic_sub_watchdog]

def int_to_signed(intval):
    if intval > 127:
        return (256-intval) * (-1)
    else:
        return intval

#mqtt stuff
def sub_cb(topic, msg, retained):
    global power_state
    runwrite = True
    hpfuncs.logprint(str(topic) + " -- " + str(msg))
################################################ 
#setpoint
    if topic == topic_sub_setp:
        try:
            values = hpfuncs.setpointVal(int(float(msg)))
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
################################################ 
#restart
    if topic == topic_sub_restart:
        try:
            machine.reset()
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False            
################################################        
# state
    elif topic == topic_sub_state:
        try:
            values = hpfuncs.stateControl(msg)
            if values == False:
                runwrite = False
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
################################################        
# swingstate
    elif topic == topic_sub_swingmode:
        try:
            values = hpfuncs.swingControl(msg)
            if values == False:
                runwrite = False
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
################################################        
# mode
    elif topic == topic_sub_mode:
        try:
            values = hpfuncs.modeControl(msg)
            if values == False:
                runwrite = False
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
################################################
# fanmode
    elif topic == topic_sub_fanmode:
        try:
            values = hpfuncs.fanControl(msg)
            if values == False:
                runwrite = False
        except Exception as e:
            hpfuncs.logprint(e)
            runwrite = False
################################################
# do init
    elif topic == topic_sub_doinit:
        myvals = hpfuncs.queryall()
        hpfuncs.logprint("initial read")
        for i in myvals:
            uart.write(bytearray(i))
            sleep(0.2)
        hpfuncs.logprint("initial read done")
        runwrite = False

################################################
# do watchdog
    elif topic == topic_sub_watchdog:
        myvals = hpfuncs.watchdog()
        for i in myvals:
            uart.write(bytearray(i))
            sleep(0.2)
        runwrite = False
################################################ 
    if runwrite == True and values != False:
        #print(values)
        for i in values:
            hpfuncs.logprint("writing: " + str(i))
            uart.write(bytearray(i))
            sleep(0.2)

        
def chunkifyarray(vals):
    val_length = len(vals)
    start = 0
    rest_size = val_length
    myresult = []
    while rest_size > 14:
        lengde= int(vals[start+6])
        chunk_size = lengde + 8
        chunk_end = start + int(vals[start+6]) + 8
        myresult.append(vals[start:chunk_end])
        start = (start + chunk_size) 
        rest_size = rest_size - chunk_size
    return myresult


# subscribe to topics
async def conn_han(client):
    for i in topics:
        await client.subscribe(i,1)
        
# first run to collect values and run watchdog
async def firstrun(client):
    firstrun = False
    await asyncio.sleep(10)
    if firstrun == False:
        ota = OTAUpdater(config['your_repo'])
        current_version = ota.get_version('/main/')
        await client.publish(config['maintopic'] + '/doinit', "firstrun version " + current_version )
        hpfuncs.logprint("init firstrun version " + current_version)
        firstrun = True
    while True:
        await asyncio.sleep(60)
        await client.publish(config['maintopic'] + '/watchdog', "get")
        hpfuncs.logprint("running watchdog..")

async def receiver(client):
    global power_state
    
    sreader = asyncio.StreamReader(uart)
    try:
        while True:
            serdata = await sreader.read(2048)
            if serdata is not None:
                readable = list()
                for i in serdata:
                    readable.append(str(int(i)))
                hpfuncs.logprint("length of data: " + str(len(readable)))
                chunks = chunkifyarray(readable)
                for data in chunks:
                    hpfuncs.logprint(data)
                    await client.publish(config['maintopic'] + '/debug/fullstring', str(data))
                    if len(data) == 17:
                        if(str(data[14]) == "187"):
                            roomtemp = int_to_signed(int(data[15]))
                            await client.publish(config['maintopic'] + '/roomtemp', str(roomtemp), qos=1)
                        if(str(data[14]) == "179"):
                            setpoint = int(data[15])
                            await client.publish(config['maintopic'] + '/setpoint/state', str(setpoint), qos=1)
                        if(str(data[14]) == "128"):
                            state = hpfuncs.inttostate[int(data[15])]
                            power_state = state
                            await client.publish(config['maintopic'] + '/state/state', str(state), qos=1)
                            if (state == "OFF"):
                                # when power state is OFF, sent unit mode also as "off"
                                await client.publish(config['maintopic'] + '/mode/state', "off", qos=1)
                        if(str(data[14]) == "160"):
                            fanmode = hpfuncs.inttofanmode[int(data[15])]
                            await client.publish(config['maintopic'] + '/fanmode/state', str(fanmode), qos=1)
                        if(str(data[14]) == "163"):
                            swingmode = hpfuncs.inttoswing[int(data[15])]
                            await client.publish(config['maintopic'] + '/swingmode/state', str(swingmode), qos=1)
                        if(str(data[14]) == "176"):
                            mode = hpfuncs.inttomode[int(data[15])]
                            # report actual mode when unit is running or "off" when it's not
                            reportedState = str(mode) if (power_state == "ON") else "off"
                            await client.publish(config['maintopic'] + '/mode/state', reportedState, qos=1) 
                        if(str(data[14]) == "190"):
                            outdoortemp = int_to_signed(int(data[15]))
                            await client.publish(config['maintopic'] + '/outdoortemp', str(outdoortemp), qos=1)
                    elif len(data) == 15:
                        if(str(data[12]) == "187"):
                            roomtemp = int_to_signed(int(data[13]))
                            await client.publish(config['maintopic'] + '/roomtemp', str(roomtemp), qos=1)
                        if(str(data[12]) == "179"):
                            setpoint = int(data[13])
                            await client.publish(config['maintopic'] + '/setpoint/state', str(setpoint), qos=1)
                        if(str(data[12]) == "128"):
                            state = hpfuncs.inttostate[int(data[13])]
                            power_state = state
                            await client.publish(config['maintopic'] + '/state/state', str(state), qos=1)
                            if (state == "OFF"):
                                # when power state is OFF, sent unit mode also as "off"
                                await client.publish(config['maintopic'] + '/mode/state', "off", qos=1)
                        if(str(data[12]) == "160"):
                            fanmode = hpfuncs.inttofanmode[int(data[13])]
                            await client.publish(config['maintopic'] + '/fanmode/state', str(fanmode), qos=1)
                        if(str(data[12]) == "163"):
                            swingmode = hpfuncs.inttoswing[int(data[13])]
                            await client.publish(config['maintopic'] + '/swingmode/state', str(swingmode), qos=1)
                        if(str(data[12]) == "176"):
                            mode = hpfuncs.inttomode[int(data[13])]
                            # report actual mode when unit is running or "off" when it's not
                            reportedState = str(mode) if (power_state == "ON") else "off"
                            await client.publish(config['maintopic'] + '/mode/state', reportedState, qos=1) 
                        if(str(data[12]) == "190"):
                            outdoortemp = int_to_signed(int(data[13]))
                            await client.publish(config['maintopic'] + '/outdoortemp', str(outdoortemp), qos=1)
     
    except Exception as e:
        hpfuncs.logprint(e)


async def mainloop(client):
    await client.connect()

config['subs_cb'] = sub_cb
config['connect_coro'] = conn_han
#config['server'] = SERVER
MQTTClient.DEBUG = True
client = MQTTClient(config)


loop = asyncio.get_event_loop()
loop.create_task(mainloop(client))
loop.create_task(receiver(client))
loop.create_task(firstrun(client))
loop.run_forever()


