from main.ota_updater import OTAUpdater
ssid = 'YOUR-SSID'
password = 'YOUR-WIFI-PASSWORD'
#REPLACE THE REPO URL WITH YOUR OWN!!
your_repo = 'https://github.com/toremick/shorai-esp32'

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
