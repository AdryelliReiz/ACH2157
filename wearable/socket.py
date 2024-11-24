import socket
import ujson
import machine
import ubinascii
import asyncio
import service
import leds
import urequests  # Para enviar requisições HTTP

# Configuração do dispositivo
print("hello")
name = "Wearable SpotDance"
device_id = ubinascii.hexlify(machine.unique_id()).decode()

# Configuração do servidor
HOST = ''  # Escuta em todas as interfaces
PORT = 8000

# URL da API para registrar a atividade
API_URL = "http://<ENDERECO_DA_API>/api/register-activity"  # Substitua pelo endpoint real

# Função para lidar com cada conexão
async def handle_connection(client_socket):
    try:
        # Receber os dados da requisição
        request = client_socket.recv(1024).decode()
        print("Requisição recebida:")
        print(request)

        # Parse do corpo da requisição para JSON
        if "POST /start" in request:
            body = request.split("\r\n\r\n")[1]
            data = ujson.loads(body)
            timer_ms = data.get("timer_ms", 0)
            user_id = data.get("userId")
            music_id = data.get("musicId")
            timer = timer_ms / 1000  # Convertendo para segundos

            print("Timer (ms):", timer_ms)
            print("Timer (s):", timer)

            # Processar o timer
            while timer > 0:
                print("Timer:", timer)
                state = service.observation_sensors()  # Verifica o estado dos sensores
                if state:
                    print("LEDs ON")
                    asyncio.create_task(leds.start_leds())  # Liga os LEDs
                else:
                    print("LEDs OFF")
                    asyncio.create_task(leds.stop_leds())  # Desliga os LEDs
                
                # Atualizar o tempo ativo durante a execução do timer
                active_time = service.get_active_time()

                # Dados para enviar durante a execução do timer
                update_data = {
                    'active_time': active_time,
                    'userId': user_id,
                    'musicId': music_id,
                    'deviceId': device_id
                }

                # Enviar os dados de atividade enquanto o timer está contando
                response = ujson.dumps(update_data)
                client_socket.sendall((
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json\r\n"
                    "Content-Length: {}\r\n\r\n{}"
                ).format(len(response), response).encode())

                await asyncio.sleep(1)  # A cada 1 segundo, atualizar

                timer -= 1  # Diminui 1 segundo

            # Após o timer terminar, registrar a atividade final
            final_active_time = service.get_active_time()
            service.reset_observation()  # Reseta os sensores

            # Enviar a atividade final para a API
            activity_data = {
                "userId": user_id,
                "musicId": music_id,
                "deviceId": device_id,
                "activeTime": final_active_time,
            }
            try:
                response = urequests.post(API_URL, json=activity_data)
                print("Resposta da API:", response.text)
                response.close()
            except Exception as e:
                print("Erro ao registrar a atividade:", e)

            # Resposta final com o tempo total
            response = ujson.dumps({'active_time': final_active_time})
            client_socket.sendall((
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                "Content-Length: {}\r\n\r\n{}"
            ).format(len(response), response).encode())

        else:
            # Resposta padrão para outras rotas
            client_socket.sendall((
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n\r\n404 Not Found"
            ).encode())

    except Exception as e:
        print("Erro ao lidar com a conexão:", e)
        # Enviar uma resposta de erro genérica para o cliente, caso haja exceções
        error_response = "HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\nContent-Length: 21\r\n\r\n500 Internal Server Error"
        client_socket.sendall(error_response.encode())
    finally:
        # Fechar o socket após o tratamento
        client_socket.close()

# Inicializar o servidor
async def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print("Servidor iniciado na porta", PORT)

        while True:
            client_socket, addr = server_socket.accept()
            print("Conexão recebida de:", addr)
            # Lidar com a conexão de forma assíncrona
            asyncio.create_task(handle_connection(client_socket))

# Função para rodar o servidor de forma assíncrona
async def run():
    await start_server()

# Iniciar a execução
if __name__ == "__main__":
    asyncio.run(run())
