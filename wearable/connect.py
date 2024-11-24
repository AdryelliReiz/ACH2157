import network
import time

#configura o dispositivo no modo estação (STA)
sta = network.WLAN(network.STA_IF)
sta.active(True)

#nome e senha da rede wifi que será conectada (2.4G)
wifi="lab8"
password="lab8arduino"

sta.connect(wifi, password)

#espera até que a conexão seja estabelecida
while not sta.isconnected():
    print('Connecting...')
    time.sleep(1)

#mostra os detalhes da conexão ao Wi-Fi
print('Connection successful')
print(sta.ifconfig())
