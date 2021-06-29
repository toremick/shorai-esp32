firmware  

Install esptool.py on your pc.

put firmware.bin i c:\  


open command prompt and run following from c:\  

`esptool.py --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 firmware.bin`
