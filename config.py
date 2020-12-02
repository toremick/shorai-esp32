from sys import platform
from main.mqtt_as import config

config['server'] = '192.168.2.30'  # Change to suit

# Set up your wifi here
config['ssid'] = 'your-ssid'
config['wifi_pw'] = 'wifi-password'