# Documentação do Projeto de Wearable Interativo para Estimular Exercícios

## Objetivo
Este projeto visa desenvolver uma roupa interativa que estimula o usuário a praticar atividades físicas por meio da dança. O wearable será capaz de monitorar os movimentos do corpo e interagir com o usuário visualmente, utilizando LEDs que reagem aos movimentos. A proposta é integrar moda e tecnologia para criar uma experiência motivadora e divertida, incentivando a prática de exercícios de forma lúdica e informativa.

## Componentes do Sistema

### 1. **Roupa**
- **Jaqueta**: Material a ser definido, que será o suporte principal para os circuitos de LEDs e acelerômetros.
- **Calça**: Estrutura já disponível, com canaletas internas conectando o circuito da tornozeleira ao circuito da jaqueta.

### 2. **Circuito Eletrônico**
- **Fitas de LED RGB Endereçável (Modelo WS2812)**: Distribuídas na roupa com 30 LEDs por metro (1 metro no total), sendo 50 cm para cada lado.
- **Acelerômetros (4x)**: Localizados em cada braço e perna para capturar e monitorar movimentos específicos.
- **ESP32**: Microcontrolador responsável pela comunicação entre os sensores e a aplicação web.
- **Cabos**: Tipos e tamanhos a serem definidos para conectar todos os componentes.

### 3. **Infraestrutura de Software**
- **Servidor Web de Conexão e Controle**: Usando o Fastify (JavaScript) para comunicação com o ESP32 e gestão dos dados, também responsável por disponibilizar páginas web com interfaces para os usuários.
- **Banco de Dados (SQLite)**: Armazena informações dos usuários e atividades realizadas.

## Funcionalidades do Wearable

### 1. **Conexão ao Spotify**
O servidor web permite que o usuário se autentique com sua conta do Spotify e forneça dados iniciais necessários para o monitoramento.

### 2. **Interface com o Usuário**
- **Tela de Autenticação**: Permite login via Spotify.
- **Tela de Configuração do Usuário**: Exibe informações de perfil e solicita o peso do usuário, necessário para cálculos de calorias.
- **Tela de Atividade**: Após autenticação e inserção do peso, o usuário pode selecionar uma música para iniciar a atividade. A interface também fornece instruções sobre o processo, incluindo botões para iniciar a atividade e sincronizar o cronômetro com o início da música.

### 3. **Reatividade das Luzes**
Os LEDs na roupa brilham em resposta ao movimento do usuário. Cada sensor de movimento controla uma seção dos LEDs, indicando visualmente a intensidade e a frequência dos movimentos em diferentes partes do corpo.

### 4. **Cronometragem e Monitoramento de Movimentos**
O wearable calcula o tempo total de atividade com base nos períodos de movimento detectados pelos acelerômetros. O cronômetro é pausado quando os sensores não detectam movimento por um tempo definido e é reativado ao detectar movimento novamente.

### 5. **Cálculo de Calorias**
Ao término de cada música, o sistema calcula uma estimativa de calorias gastas com base no tempo de atividade e no peso do usuário, utilizando a fórmula:

**DE = METs da atividade x Peso Corporal (Kg) x Duração (min/60)**

Exemplo: Dança de salão rápida tem um MET de 4,5.

### 6. **Armazenamento e Consulta de Dados**
As informações de autenticação, músicas tocadas, tempo ativo e calorias gastas são armazenadas no banco de dados. A interface permite que o usuário visualize dados históricos, incluindo o total de calorias gastas, quantidade de atividades realizadas e o tempo total ativo.

## Estrutura do Banco de Dados

### 1. **Entidade Usuário**
- **Atributos**: ID, nome, peso

### 2. **Entidade Atividade**
- **Atributos**: ID da atividade, ID do usuário, identificador da música, tempo ativo (em segundos) e calorias gastas durante a atividade.

---

### Considerações Finais
O projeto visa não só proporcionar uma experiência interativa e divertida, mas também incentivar hábitos mais saudáveis por meio de um wearable que integra funcionalidades de monitoramento e feedback em tempo real. A combinação de moda e tecnologia oferece ao usuário uma maneira inovadora de se engajar em exercícios físicos, enquanto a gamificação e a integração com o Spotify tornam o processo ainda mais envolvente.
