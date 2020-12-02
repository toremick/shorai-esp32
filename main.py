import ConnectWiFi
ConnectWiFi.connect()

def start():
    from main import inithp
    inithp.start_handshake()
    from main import heatpump


start()