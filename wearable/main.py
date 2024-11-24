import asyncio
import leds
import connect
import socket
#import routes

async def main():
    leds.esp_on_led_effect()
    await asyncio.sleep(2)  # Pequeno delay para inicialização
    # Executar o servidor
    try:
        asyncio.run(socket.start_server())
    except KeyboardInterrupt:
        print("\nServidor encerrado.")

if __name__ == "__main__":
    asyncio.run(main())
