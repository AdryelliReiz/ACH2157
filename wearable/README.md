# Wearable

Projeto desenvolvido em MicroPython para ser executado em um ESP32 com suporte ao Microdot. Este wearable utiliza LEDs e acelerômetros para capturar movimentos e exibir padrões de luz.

## Dispositivos Conectados

- **ESP32**: Microcontrolador principal.
- **Duas fitas de LEDs**: Controladas individualmente.
- **Dois acelerômetros**: Para detecção de movimentos.
- **Fonte de alimentação**: Power bank.

## Conexões

| Conexão ESP32 | Acelerômetro 1 (ac-1) | Acelerômetro 2 (ac-2) | Fita LED 1 (fl-1) | Fita LED 2 (fl-2) | Power Bank (PB) | Observações                  |
|---------------|------------------------|------------------------|-------------------|-------------------|-----------------|-----------------------------|
| 5V            | ---                    | ---                    | 5V                | 5V                | 5V*             | Conexão principal de energia |
| 3V3           | 3V3                    | 3V3, AD0               | ---               | ---               | ---             | Alimentação lógica           |
| GND           | GND                    | GND                    | GND               | GND               | GND             | Terra comum                  |
| GPIO (SCL)    | SCL                    | SCL                    | ---               | ---               | ---             | Comunicação I2C              |
| GPIO (SDA)    | SDA                    | SDA                    | ---               | ---               | ---             | Comunicação I2C              |
| GPIO (Data)   | ---                    | ---                    | Di                | ---               | ---             | Envio de dados para LEDs     |
| GPIO (Data)   | ---                    | ---                    | ---               | Di                | ---             | Envio de dados para LEDs     |

- Os pinos GPIO 2 e 4 do ESP32 foram configurados para enviar dados às fitas de LEDs.

## Endpoints da API

O dispositivo fornece uma API para interação via HTTP, permitindo iniciar uma animação e monitorar o tempo de atividade.

### `/start`

**Métodos**: `POST`, `PUT`  
**Parâmetros**:
- `timer_ms` (int): Duração da música em milissegundos.

**Status de Resposta**:
- `200`: Requisição bem-sucedida.
- `400`: Parâmetros inválidos.
- `500`: Erro interno no servidor.

---

### `/active_time`

**Método**: `GET`  
**Descrição**: Retorna o tempo ativo dos movimentos registrados.

**Status de Resposta**:
- `204`: Sucesso, tempo ativo retornado.
- `400`: Sensores ainda estão ativos, sem resultados disponíveis.

## Configurações

### Conexão Wi-Fi
No arquivo `connect.py`, insira as credenciais do Wi-Fi:
```python
WIFI = "nome_do_wifi"
PASSWORD = "senha_do_wifi"
```
Lembrando que precisa ser um Wi-Fi que tenha conexão 2.4 GHz.

### Porta do Servidor
No arquivo `routes.py`, altere o valor da variável `PORT` para configurar a porta do servidor:
```python
PORT = 8000  # Exemplo
```

### Configuração dos LEDs
No arquivo `leds.py`, personalize a sequência de cores exibida pelas fitas de LEDs. Também é possível alterar quais pinos estão sendo usados para transmitir as informações às fitas de LEDs.

## Dependências

- **MicroPython**: O código foi desenvolvido para ser executado em MicroPython.
- **Biblioteca Microdot**: Utilizada para configurar o servidor HTTP.
- **neopixel**: Biblioteca para controlar os LEDs.