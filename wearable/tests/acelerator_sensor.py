from machine import Pin, I2C
import time
import math

# Endereço I2C padrão do MPU-9250
MPU9250_ADDRESS = 0x68

# Registradores do acelerômetro
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
PWR_MGMT_1 = 0x6B

# Inicializa o I2C para o ESP32
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Função para ler dois bytes e converter para valor inteiro
def read_word(reg_addr):
    high = i2c.readfrom_mem(MPU9250_ADDRESS, reg_addr, 1)[0]
    low = i2c.readfrom_mem(MPU9250_ADDRESS, reg_addr + 1, 1)[0]
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

# Inicializa o MPU-9250
def init_mpu():
    # Escreve 0 no registrador de gerenciamento de energia para ativar o sensor
    i2c.writeto_mem(MPU9250_ADDRESS, PWR_MGMT_1, b'\x00')
    time.sleep(0.1)

# Função para obter os valores de aceleração em g (gravidade)
def get_accel_data():
    accel_x = read_word(ACCEL_XOUT_H) / 16384.0  # Dividido pelo fator de escala para obter valores em g
    accel_y = read_word(ACCEL_YOUT_H) / 16384.0
    accel_z = read_word(ACCEL_ZOUT_H) / 16384.0
    return accel_x, accel_y, accel_z

# Inicializa o MPU-9250
init_mpu()

ant_ax = 0
ant_ay = 0
ant_az = 0

#diferença para aceitar o movimento
DIFERENCIAL = 0.2
tempo_ativo = 0.0
tempo_ocioso = 0.0
tempo_max_ocioso = 3

# Loop para ler e exibir os dados do acelerômetro
while True:
    ax, ay, az = get_accel_data()
    print("Aceleração em g -> X: {:.2f}, Y: {:.2f}, Z: {:.2f}".format(ax, ay, az))
    
    #se for a primeira interação
    if(ant_ax != 0 and ant_ay != 0 and ant_az != 0):
        #vamos calcular se teve uma diferença entre os movimentos
        dif_x = abs(ant_ax - ax)
        dif_y = abs(ant_ay - ay)
        dif_z = abs(ant_az - az)
        if(dif_x > DIFERENCIAL or dif_y > DIFERENCIAL or dif_z > DIFERENCIAL):
            #teve movimento
            print("Movimento detectado")
            tempo_ativo += 0.5
            tempo_ocioso = 0
        else:
            if(tempo_ocioso >= tempo_max_ocioso):
                print("FIM | Tempo total ativo: ", tempo_ativo)
                tempo_ativo = 0
                tempo_ocioso = 0
            else:
                tempo_ocioso += 0.5
    ant_ax = ax
    ant_ay = ay
    ant_az = az
    
    time.sleep(0.5)

