from microdot import Microdot, Response
import ubinascii
import machine
import ujson
import leds
import asyncio
import service

print("hello")
name = "Wearable SpotDance"
device_id = ubinascii.hexlify(machine.unique_id()).decode()

app = Microdot()

@app.route('/')
async def home(request):
    return Response("Você está conectado com {}!".format(name))

@app.route('/start', methods=['POST'])
async def start(request):
    print("Rota chamada")
    data = ujson.loads(request.body.decode())
    #music_id = data.get("musicId")
    #user_id = data.get("userId")
    timer_ms = data.get("timer_ms")
    timer = timer_ms / 1000

    #print("Music ID:", music_id)
    #print("User ID:", user_id)
    print("Timer (ms):", timer_ms)
    print("Timer (s):", timer)

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

    service.reset_oberservation()

    return Response.json({'active_time': active_time})
        

# Inicia o servidor na porta 8000
app.run(port=8000)
print("Iniciando servidor")

