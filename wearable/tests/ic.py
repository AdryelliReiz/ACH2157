import network
import uasyncio
import time
import json
import urequests
from mdns_client import Client
from mdns_client.service_discovery import ServiceResponse
from mdns_client.service_discovery.txt_discovery import TXTServiceDiscovery
from microdot import Microdot, Response

TD = {
  "@context": [
    "https://www.w3.org/2019/wot/td/v1",
    {
      "language": "en"
    }
  ],
  "title": "ESP32 Device",
  "id": "urn:dev:ops:ESP32-001",
  "base": "http://esp32.local",
  "security": ["nosec_sc"],
  "properties": {
    "getThingDescription": {
      "type": "string",
      "title": "Get Thing Description",
      "description": "Provides the Thing Description of the device",
      "readOnly": True,
      "forms": [
        {
          "href": "/getThingDescription",
          "contentType": "application/json",
          "op": "readproperty"
        }
      ]
    }
  },
  "actions": {
    "doSomething": {
      "title": "Do something",
      "description": "Does something",
      "forms": [
        {
          "href": "/doSomething",
          "contentType": "application/json",
          "op": "invokeaction"
        }
      ]
    }
  },
  "events": {},
  "links": [
    {
      "rel": "properties",
      "href": "/properties"
    },
    {
      "rel": "actions",
      "href": "/actions"
    },
    {
      "rel": "events",
      "href": "/events"
    }
  ],
  "securityDefinitions": {
    "nosec_sc": {
      "scheme": "nosec"
    }
  }
}

print("Starting mDNS on ESP32")

# =============================== < wi-fi > ===============================
# Conectar ao Wi-Fi
ssid = "lab8"
password = "lab8arduino"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    print("Conectando...")
    time.sleep(1)

print("Conectado! Configurações de IP:", wlan.ifconfig())

own_ip_address = wlan.ifconfig()[0]

print("My IP address: ", own_ip_address)

# =============================== < microdot > ===============================
# Iniciando servidor
app = Microdot()
Response.default_content_type = 'application/json'

# Rota principal
@app.route('/')
async def handle_root(request):
    return {"message": "Hello from ESP32! This ESP acts as both a client and a server."}

# Rota para Thing Description
@app.route('/thing-description')
async def get_thing_description(request):
    return json.dumps(TD)

# Rota para executar uma ação (buzz)
@app.route('/do-something')
async def do_something(request):
    print("Executing action: Buzz... (simulated)")
    return {"message": "Action executed: buzz..."}

# Rota para tratar caminhos não encontrados
@app.route('<path:path>')
async def handle_not_found(request, path):
    return {"error": "Not found"}, 404

# =============================== < mDNS > ===============================
# Inicializar o cliente mDNS
loop = uasyncio.get_event_loop()
client = Client(own_ip_address)
discovery = TXTServiceDiscovery(client)

class ServiceMonitor:
    def service_added(self, service: ServiceResponse) -> None:
        print("Service added: {}".format(service))

    def service_updated(self, service: ServiceResponse) -> None:
        print("Service updated: {}".format(service))

    def service_removed(self, service: ServiceResponse) -> None:
        print("Service removed: {}".format(service))

def is_same_subnet(ip1, ip2):
    # Verifica se dois IPs estão na mesma sub-rede (classe C).
    return ip1.split('.')[:3] == ip2.split('.')[:3]

def is_a_valid_ip(ip):
    print(ip)
    type_ = ip.split('.')[:3]
    return (type_ != '172' and type_ != '100')

async def discover():
    print("Encontrando Thing Directory...")
    serviceIsFinded = False
    discovery.add_service_monitor(ServiceMonitor())

    # Loop até encontrar o serviço desejado
    while not serviceIsFinded:
        await discovery.query("_wot", "_tcp")
        services = discovery.current("_wot", "_tcp")

        if services:
            print(f"Found services of type '_wot._tcp': {services}")
            service = services[0]  # Seleciona o primeiro serviço encontrado

            # Buscar o IP certo na mesma sub-rede que o ESP32
            ip_address = None
            for ip in service.ips:
                if is_a_valid_ip(ip):
                    ip_address = ip
                    break

            if ip_address:
                print(f"Using IP: {ip_address} on port {service.port}")
                url = f"http://{ip_address}:{service.port}/things/{TD.id}"
                headers = {"Content-Type": "application/json"}
                payload = {"status": "updated", "message": "Hello from ESP32!"}
                print(f"Sending PUT request to {url}...")

                try:
                    response = urequests.put(url, data=json.dumps(TD), headers=headers)
                    print("Response status:", response.status_code)
                    print("Response body:", response.text)
                    response.close()
                except Exception as e:
                    print("Failed to send PUT request:", e)

                serviceIsFinded = True
            else:
                print("No matching IP found in the same subnet.")
                await uasyncio.sleep(5)
        else:
            print("No services found. Retrying in 5 seconds...")
            await uasyncio.sleep(5)

async def start_server():
    print("Servidor iniciado na porta 80...")
    await app.start_server(host='0.0.0.0', port=80)

async def main():
    await uasyncio.gather(
        start_server(),
        discover() # Execute a descoberta de serviços
    )
    #asyncio.create_task(discover_services())  # Descoberta em segundo plano
    #await start_server()

uasyncio.run(main())

