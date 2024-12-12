import asyncio
import leds
import connect
import routes

async def main():
    leds.esp_on_led_effect()
    await asyncio.sleep(2)  # Pequeno delay para inicialização
    
    # Executar o servidor de forma assíncrona
    try:
        await routes.start_server()  # Espera pela execução do servidor
    except KeyboardInterrupt:
        print("\nServidor encerrado.")

if __name__ == "__main__":
    asyncio.run(main())  # Inicia o loop de eventos

