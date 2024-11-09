import neopixel
import machine
import time

def fade (np, f):
    aux=[0,0,0]
    for i in range(0,np.n):
        aux[0]=np[i][0]//f
        aux[1]=np[i][1]//f
        aux[2]=np[i][2]//f
        np[i]=tuple(aux)

def knightRider(np, f, color=(200,0,0)):
    for i in range(0,np.n):
        fade(np, f)
        np[i]=color
        np.write()
        time.sleep(0.2)
    for i in reversed(range(0, np.n)):
        fade(np, f)
        np[i]=color
        np.write()
        time.sleep(0.2)

def cKnight(np, f, color=(200,0,0)):
    while (True):
        knightRider(np, f, color)

def rainbow(np):
    # Define the RGB colors for the rainbow
    rainbow_colors = [
        (255, 0, 0),    # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (75, 0, 130),   # Indigo
        (148, 0, 211)   # Violet
    ]
    count = 0
    num_colors = len(rainbow_colors)

    while True:
        # Apply a color from the rainbow to each LED, offset by `count`
        for i in range(np.n):
            # Select color with wrap-around using modulo
            color_index = (i + count) % num_colors
            np[i] = rainbow_colors[color_index]

        np.write()  # Update all LEDs at once
        time.sleep(0.1)  # Delay for smoother transition
        count = (count + 1) % num_colors  # Increment and wrap count


nnp=5 # number of neopixels
npp=2 # neopixels data pin

np=neopixel.NeoPixel(machine.Pin(npp), nnp)
