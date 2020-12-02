# shorai-esp32
esp32 connected to shorai heat pump

This works great for me, but is at your own risk!


### PCB Schematic
![PCB Schematic](images/schematic.PNG?raw=true "PCB Schematic")

### PCB Layout
![PCB layout](images/pcb.PNG?raw=true "PCB layout")
U5 is a jumper, close the jumper to be powered from the heatpump. Remove jumper when powered from usb.


### Parts list

* 1 x ESP32-DevKitC
* 2 x Optocoupler ![EL817A](https://www.ebay.com/itm/Straight-Plug-Optocoupler-EL817-A-B-C-D-F-DIP-4-Compatible-PC817-Isolator/253795050804?hash=item3b175d2534:g:LjcAAOSwXVNbY~z3)
* 4 x 0.25w 1K resistors
* 1 x 0.25w 470R resistor
* 1 x 0.25w 10K resistor
* 1 x 0.25w 220R
* 2 x 100uF (11mmx5mm) Capacitor 
* and 2.54mm header pins and sockets
