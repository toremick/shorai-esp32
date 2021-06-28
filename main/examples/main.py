from main.ota_updater import OTAUpdater

ssid = 'YOUR-SSID'
password = 'YOUR-WIFI-PASSWORD'


# MQTT settings
config['server'] = '192.168.2.30'  # Change to suit
config['maintopic'] = 'heatpump'
# uncomment next two lines and set credentials if your mqtt broker uses authentication.
# config['user'] = 'mqtt-username'
# config['password'] = 'mqtt-password'

# repo
# REPLACE THE REPO URL WITH YOUR OWN!!
# OR ELSE YOU WILL RECIEVE UPDATES FROM THIS REPO AT A REBOOT
your_repo = 'https://github.com/toremick/shorai-esp32'



config['ssid'] = ssid
config['wifi_pw'] = password



def download_and_install_update_if_available():
    o = OTAUpdater(your_repo)
    o.check_for_update_to_install_during_next_reboot(ssid, password)
    o.download_and_install_update_if_available(ssid, password)
     
def start():
    from main import inithp
    inithp.start_handshake()
    from main import heatpump
    
    

def boot():
    download_and_install_update_if_available()
    start()


boot()
