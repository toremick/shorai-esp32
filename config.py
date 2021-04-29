from sys import platform
from main.mqtt_as import config
# mqtt settings
config['server'] = '192.168.2.30'  # Change to suit
config['maintopic'] = 'heatpump'

# uncomment next two lines and set credentials if your mqtt broker uses authentication.
# config['user'] = 'mqtt-username'
# config['password'] = 'mqtt-password'

# Set up your wifi here
config['ssid'] = 'your-ssid'
config['wifi_pw'] = 'wifi-password'
