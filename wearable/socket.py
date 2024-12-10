import usocket as socket
import ujson
import machine
import ubinascii
import uasyncio as asyncio
import service
import leds
import urequests  # Para enviar requisições HTTP
import uhashlib as hashlib
import ubinascii

# Definir o WebSocket
class WebSocketServer:
    def __init__(self, port):
        self.port = port
        self.server = None

    def start(self):
        # Criar o socket
        addr = socket.getaddrinfo('0.0.0.0', self.port)[0][-1]
        self.server = socket.socket()
        self.server.bind(addr)
        self.server.listen(1)
        print('Servidor WebSocket iniciado na porta', self.port)

        while True:
            client, addr = self.server.accept()
            print('Conexão de', addr)
            self.handle_client(client)

    def handle_client(self, client):
        # Inicializar a conexão WebSocket
        self.handshake(client)

        try:
            while True:
                # Receber a mensagem do cliente
                data = self.receive_message(client)
                if data:
                    message = json.loads(data)
                    print('Mensagem recebida:', message)
                    
                    if message.get('type') == 'start-activity':
                        # Exibir a mensagem quando o tipo for 'start-activity'
                        timer_ms = data.get("timer_ms", 0)
                        user_id = data.get("userId")
                        music_id = data.get("musicId")
                        timer = timer_ms / 1000

                        print("Timer (s):", timer)

                    while timer > 0:
                        state = service.observation_sensors()
                        if state:
                            asyncio.create_task(leds.start_leds())
                        else:
                            asyncio.create_task(leds.stop_leds())

                        active_time = service.get_active_time()
                        update_data = {
                            'type': 'sync',
                            'active_time': active_time,
                            'userId': user_id,
                            'musicId': music_id,
                            'deviceId': device_id
                        }
                        response = ujson.dumps(update_data)
                        client_socket.sendall((
                            "HTTP/1.1 200 OK\r\n"
                            "Content-Type: application/json\r\n"
                            "Content-Length: {}\r\n\r\n{}"
                        ).format(len(response), response).encode())

                        await asyncio.sleep(1)
                        timer -= 1

                    final_active_time = service.get_active_time()
                    service.reset_observation()

                    activity_data = {
                        "userId": user_id,
                        "musicId": music_id,
                        "deviceId": device_id,
                        "activeTime": final_active_time,
                    }
                    try:
                        response = urequests.post(API_URL, json=activity_data)
                        print("Resposta da API:", response.text)

                        # api retorna { id: result.lastID, userId, musicId, duration, date, caloriesBurned }
                        # enviar duration e caloriesBurned via socket com type 'activity-finished'
                        response.close()
                    except Exception as e:
                        print("Erro ao registrar a atividade:", e)

                    response = ujson.dumps({'active_time': final_active_time})
                    client_socket.send((
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/json\r\n"
                        "Content-Length: {}\r\n\r\n{}"
                    ).format(len(response), response).encode())
                        
                time.sleep(1)
        except Exception as e:
            print('Erro no cliente:', e)
        finally:
            client.close()

    def handshake(self, client):
        # Realizar o "handshake" WebSocket
        client.send(b"HTTP/1.1 101 Switching Protocols\r\n"
                    b"Upgrade: websocket\r\n"
                    b"Connection: Upgrade\r\n"
                    b"Sec-WebSocket-Accept: dGhlIHNhbXBsZSBub25jZQ==\r\n\r\n")

    def receive_message(self, client):
        # Lê os dados do WebSocket
        data = client.recv(1024)
        return data.decode('utf-8')

# Criar o servidor WebSocket e iniciar na porta 8000
ws_server = WebSocketServer(port=8000)
ws_server.start()
