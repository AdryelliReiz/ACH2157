from microdot import Microdot, Response
import ubinascii
import machine
import ujson
import leds
import asyncio
import service

# Configuração inicial
PORT=8000 # Porta do servidor
name = "Wearable SpotDance"
device_id = ubinascii.hexlify(machine.unique_id()).decode()
active_time = 0
still_active = False

app = Microdot()

# Função para adicionar cabeçalhos CORS nas respostas
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Permite todas as origens
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    print("Adicionando cabeçalhos CORS: ", response.headers)  # Log para diagnosticar
    return response

# Middleware para adicionar os cabeçalhos CORS em todas as respostas
@app.before_request
def before_request(request):
    # Apenas adicionar os cabeçalhos CORS, sem bloquear a execução da rota
    pass

# Rota principal (home)
@app.route('/')
async def home(request):
    response = Response(f"Você está conectado com {name}!")
    return add_cors_headers(response)

# Rota de start, onde o timer é configurado
@app.route('/start', methods=['POST', 'PUT'])  # Aceita POST e PUT
async def start(request):
    global active_time, still_active
    
    try:
        # Tenta ler o corpo da requisição
        data = ujson.loads(request.body.decode())
        timer_ms = data.get("timer_ms")
        timer = timer_ms / 1000  # Converte milissegundos para segundos

        print("Timer (ms):", timer_ms)
        print("Timer (s):", timer)

        # Verifica se o timer é um valor válido
        if timer <= 0:
            response = Response("O timer deve ser maior que zero.", status_code=400)
        else:
            # Define que os sensores estão ativos
            still_active = True
            # Responde que os sensores estão ativos
            response = Response.json({"message": "Sensores ativados!", "status": "started"})

        add_cors_headers(response)

        # Laço para executar o timer
        while timer > 0:
            print("timer:", timer)
            state = service.observation_sensors()
            if state:
                print("leds on")
                asyncio.create_task(leds.start_leds())
            else:
                print("leds off")
                asyncio.create_task(leds.stop_leds())
            await asyncio.sleep(0.5)
            timer -= 0.5

        active_time = service.get_active_time()
        service.reset_observation()
    
    except Exception as e:
        print(f"Erro ao processar requisição: {e}")
        return Response("Erro no processamento", status_code=500)

@app.route('/active_time', methods=['GET'])
async def get_active_time(request):
    global active_time, still_active
    
    # Durante 10s espera e verifica se a observação ainda está ativa
    for _ in range(10):
        if still_active:
            await asyncio.sleep(1)
        else:
            # Se os sensores não estão mais ativos, retorna o tempo ativo final
            active_time = service.get_active_time()
            response = Response.json({"active_time": active_time})
            return add_cors_headers(response)
    
    return Response("Sensores não estão ativos.", status_code=400)
        

# Tratamento de preflight CORS com método OPTIONS
@app.route('/start', methods=['OPTIONS'])
async def options(request):
    print("Requisição OPTIONS recebida para /start")
    response = Response()
    # Adiciona os cabeçalhos CORS para preflight
    return add_cors_headers(response)

# Função para iniciar o servidor de forma assíncrona
async def start_server():
    print("Iniciando servidor...")
    await app.run(host='0.0.0.0', port=PORT)  # Usando o método assíncrono

