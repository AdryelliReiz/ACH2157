import neopixel
import machine
import asyncio

nnp = 10  # Número de LEDs
npp1 = 2  # Pino de dados para a fita 1
npp2 = 4  # Pino de dados para a fita 2

np_f1 = neopixel.NeoPixel(machine.Pin(npp1), nnp)
np_f2 = neopixel.NeoPixel(machine.Pin(npp2), nnp)

async def neon_transition(np_f1, np_f2, colors, duration=0.5, steps=10):
    """
    Transição cíclica rápida entre rosa e verde para todos os LEDs, com duração de 0.5 segundo.
    """
    total_steps = steps * len(colors)
    step_delay = duration / total_steps  # Ajuste do tempo entre os passos

    for i in range(len(colors)):
        start_color = colors[i]
        end_color = colors[(i + 1) % len(colors)]

        for step in range(steps):
            # Interpolação de cores entre o início e o fim da transição
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (step / steps))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (step / steps))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (step / steps))

            for j in range(np_f1.n):
                np_f1[j] = (r, g, b)
                np_f2[j] = (r, g, b)
            np_f1.write()
            np_f2.write()
            await asyncio.sleep(step_delay)

async def fade_out(np_f1, np_f2, duration=0.3, steps=10):
    """
    Apaga os LEDs suavemente.
    """
    for step in range(steps):
        brightness = 1 - step / steps
        for i in range(np_f1.n):
            current_color = np_f1[i]
            np_f1[i] = (
                int(current_color[0] * brightness),
                int(current_color[1] * brightness),
                int(current_color[2] * brightness)
            )
            np_f2[i] = (
                int(current_color[0] * brightness),
                int(current_color[1] * brightness),
                int(current_color[2] * brightness)
            )
        np_f1.write()
        np_f2.write()
        await asyncio.sleep(duration / steps)

async def start_leds():
    """
    Inicia os LEDs com um efeito neon rápido entre rosa e verde.
    """
    colors = [(255, 0, 255), (0, 255, 0)]  # Cores neon rosa e verde
    await neon_transition(np_f1, np_f2, colors, duration=0.5)  # Duração ajustada para meio segundo

async def stop_leds():
    """
    Apaga os LEDs com um efeito de fade-out.
    """
    await fade_out(np_f1, np_f2)


async def esp_on_led_effect():
    start_leds()
    stop_leds()