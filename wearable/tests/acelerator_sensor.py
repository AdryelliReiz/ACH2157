from machine import Pin, I2C
import time
import asyncio
import leds

# Endereços I2C dos dois MPU-9250
MPU1_ADDRESS = 0x68  # Primeiro sensor (AD0 = GND)
MPU2_ADDRESS = 0x69  # Segundo sensor (AD0 = 3.3V)

# Registradores do acelerômetro
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
PWR_MGMT_1 = 0x6B

# Inicializa o I2C para o ESP32
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

devices = i2c.scan()
if devices:
    print("Dispositivos encontrados:")
    for device in devices:
        print("Endereço I2C:", hex(device))
else:
    print("Nenhum dispositivo I2C encontrado.")

# Função para ler dois bytes e converter para valor inteiro
def read_word(i2c, addr, reg_addr):
    high = i2c.readfrom_mem(addr, reg_addr, 1)[0]
    low = i2c.readfrom_mem(addr, reg_addr + 1, 1)[0]
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

# Inicializa o MPU-9250
def init_mpu(i2c, addr):
    try:
        # Escreve 0 no registrador de gerenciamento de energia para ativar o sensor
        i2c.writeto_mem(addr, PWR_MGMT_1, b'\x00')
        time.sleep(0.1)
        
        # Tenta ler o registrador WHO_AM_I para verificar a resposta do sensor
        who_am_i = i2c.readfrom_mem(addr, 0x75, 1)  # Registrador WHO_AM_I
        print(f"Valor WHO_AM_I: {who_am_i[0]}")
        
        if who_am_i[0] != 0x73:  # O valor esperado para MPU-9250 é 0x71
            raise ValueError("MPU-9250 não respondeu corretamente.")
    except OSError as e:
        print(f"Erro de comunicação I2C: {e}")
        raise



# Função para obter os valores de aceleração em g (gravidade)
def get_accel_data(i2c, addr):
    accel_x = read_word(i2c, addr, ACCEL_XOUT_H) / 16384.0  # Dividido pelo fator de escala para obter valores em g
    accel_y = read_word(i2c, addr, ACCEL_YOUT_H) / 16384.0
    accel_z = read_word(i2c, addr, ACCEL_ZOUT_H) / 16384.0
    return accel_x, accel_y, accel_z

# Inicializa os dois sensores
init_mpu(i2c, MPU1_ADDRESS)
init_mpu(i2c, MPU2_ADDRESS)

ant_ax1 = ant_ay1 = ant_az1 = 0
ant_ax2 = ant_ay2 = ant_az2 = 0

# Diferença para aceitar o movimento
DIFERENCIAL = 0.2
tempo_ativo = 0
ocioso1 = 0
ocioso2 = 0

def observation_sensors():
    global ant_ax1, ant_ay1, ant_az1, ant_ax2, ant_ay2, ant_az2
    global tempo_ativo, ocioso1, ocioso2
    # Leitura do primeiro sensor
    ax1, ay1, az1 = get_accel_data(i2c, MPU1_ADDRESS)
    # Leitura do segundo sensor
    ax2, ay2, az2 = get_accel_data(i2c, MPU2_ADDRESS)

    # Para o primeiro sensor
    if ant_ax1 != 0 and ant_ay1 != 0 and ant_az1 != 0:
        dif_x1 = abs(ant_ax1 - ax1)
        dif_y1 = abs(ant_ay1 - ay1)
        dif_z1 = abs(ant_az1 - az1)
        if dif_x1 > DIFERENCIAL or dif_y1 > DIFERENCIAL or dif_z1 > DIFERENCIAL:
            ocioso1 = 0
        else:
            ocioso1 = 1

    # Para o segundo sensor
    if ant_ax2 != 0 and ant_ay2 != 0 and ant_az2 != 0:
        dif_x2 = abs(ant_ax2 - ax2)
        dif_y2 = abs(ant_ay2 - ay2)
        dif_z2 = abs(ant_az2 - az2)
        if dif_x2 > DIFERENCIAL or dif_y2 > DIFERENCIAL or dif_z2 > DIFERENCIAL:
            ocioso2 = 0
        else:
            ocioso2 = 1

    # Atualiza os valores anteriores
    ant_ax1, ant_ay1, ant_az1 = ax1, ay1, az1
    ant_ax2, ant_ay2, ant_az2 = ax2, ay2, az2

    # Verifica se ambos os sensores estão ociosos antes de retornar
    if ocioso1 and ocioso2:
        return False

    tempo_ativo += 0.5
    return True  # Se não estiver ocioso, retorna False

def get_active_time():
    return tempo_ativo

def reset_oberservation():
    global ant_ax1, ant_ay1, ant_az1, ant_ax2, ant_ay2, ant_az2
    global tempo_ativo, ocioso1, ocioso2

    ant_ax1 = ant_ay1 = ant_az1 = 0
    ant_ax2 = ant_ay2 = ant_az2 = 0
    tempo_ativo = 0
    ocioso1 = 0
    ocioso2 = 0

    return

async def main():
    while True:
        state = observation_sensors()
        if state:
            asyncio.create_task(leds.start_leds())
        else:
            asyncio.create_task(leds.stop_leds())
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())  # Inicia o loop de eventos
