# Documentação da API

Explicarei como subir esse servidor para ficar disponível ao Wearable.

## Iniciando o Servidor

Para iniciar o servidor, siga os passos abaixo:

1. Certifique-se de ter o Node.js instalado em sua máquina.
2. Navegue até o diretório do projeto:
    ```bash
    cd server
    ```
3. Instale as dependências do projeto:
    ```bash
    npm install
    ```
4. Inicie o servidor:
    ```bash
    npm run start
    ```
    ou inicie o servidor em modo de desenvolvimento
    ```bash
    npm run dev
    ```


O servidor estará rodando na porta `8080`.

## Configuração da aplicação Spotify

No arquivo ``public/index.html`, é necessário colocar o clientId referente a sua aplicação do Spotify. Você consegue criar e configurar uma aplicação [aqui](https://developer.spotify.com/dashboard).

## Rotas do Web Site

### Rotas Web App

Este módulo fornece rotas para servir páginas HTML no servidor.

---

#### 1. Página Inicial

**Rota:** `GET /`

**Descrição:** Serve a página inicial do aplicativo.

**Resposta:**
- `200 OK`: Retorna o arquivo `index.html`.

---

#### 2. Página de Perfil

**Rota:** `GET /profile`

**Descrição:** Serve a página de perfil do usuário.

**Resposta:**
- `200 OK`: Retorna o arquivo `profile.html`.

---

#### 3. Página de Atividades

**Rota:** `GET /activity`

**Descrição:** Serve a página de atividades do usuário.

**Resposta:**
- `200 OK`: Retorna o arquivo `activity.html`.


## Rotas da API

### Rotas Users

Este módulo fornece rotas para manipulação de dados de usuários, como criação, listagem, atualização e remoção de usuários, além de cálculo de atividades associadas ao usuário.

---

#### 1. Adicionar Novo Usuário

**Rota:** `POST /api/users`

**Descrição:** Adiciona um novo usuário ao banco de dados. Caso o usuário já exista, retorna as informações de atividades do usuário.

**Parâmetros do Corpo da Requisição (JSON):**
- `id` (obrigatório, string): Identificador único do usuário.
- `name` (obrigatório, string): Nome do usuário.

**Resposta:**
- `200 OK`: Retorna os dados do usuário criado ou, se já existir, as informações de atividades, duração total e calorias queimadas.
- `400 Bad Request`: Falta de parâmetros obrigatórios (`id` e/ou `name`).

---

#### 2. Listar Todos os Usuários

**Rota:** `GET /api/users`

**Descrição:** Retorna uma lista de todos os usuários registrados.

**Parâmetros:** Nenhum

**Resposta:**
- `200 OK`: Array de objetos de usuários.

---

#### 3. Obter Usuário por ID

**Rota:** `GET /api/users/:id`

**Descrição:** Retorna os dados de um usuário específico com informações de atividades associadas, como duração total e calorias queimadas.

**Parâmetros da URL:**
- `id` (obrigatório, string): Identificador do usuário.

**Resposta:**
- `200 OK`: Dados do usuário e suas atividades, duração total e calorias queimadas.
- `404 Not Found`: Usuário não encontrado.

---

#### 4. Atualizar Peso do Usuário

**Rota:** `PUT /api/users/:id`

**Descrição:** Atualiza o peso do usuário.

**Parâmetros da URL:**
- `id` (obrigatório, string): Identificador do usuário.

**Parâmetros do Corpo da Requisição (JSON):**
- `weight` (obrigatório, number): Peso do usuário.

**Resposta:**
- `204 No Content`: Peso atualizado com sucesso.
- `400 Bad Request`: Falta o parâmetro obrigatório `weight`.
- `404 Not Found`: Usuário não encontrado.

---

#### 5. Deletar Usuário

**Rota:** `DELETE /api/users/:id`

**Descrição:** Remove um usuário do banco de dados e deleta todas as atividades associadas.

**Parâmetros da URL:**
- `id` (obrigatório, string): Identificador do usuário.

**Resposta:**
- `200 OK`: Retorna o ID do usuário deletado.
- `404 Not Found`: Usuário não encontrado.

### Rotas Activities

Este módulo fornece rotas para a manipulação de dados de atividades físicas dos usuários, como registro de atividades, listagem de atividades, e remoção de atividades específicas ou todas as atividades de um usuário.

---

#### 1. Registrar uma Atividade

**Rota:** `POST /api/activities`

**Descrição:** Registra uma nova atividade realizada por um usuário, calculando as calorias queimadas com base no tempo de duração e peso do usuário.

**Parâmetros do Corpo da Requisição (JSON):**
- `userId` (obrigatório, string): Identificador do usuário que realizou a atividade.
- `musicId` (obrigatório, string): Identificador da música associada à atividade.
- `duration` (obrigatório, número): Duração da atividade em segundos.
- `date` (obrigatório, string): Data da atividade (formato `YYYY-MM-DD`).

**Resposta:**
- `200 OK`: Retorna os dados da atividade registrada.
- `400 Bad Request`: Falta de parâmetros obrigatórios.
- `404 Not Found`: Usuário não encontrado.

---

#### 2. Listar Todas as Atividades

**Rota:** `GET /api/activities`

**Descrição:** Retorna uma lista de todas as atividades registradas no sistema.

**Parâmetros:** Nenhum

**Resposta:**
- `200 OK`: Array de objetos de atividades.

---

#### 3. Listar Atividades de um Usuário Específico

**Rota:** `GET /api/users/:id/activities`

**Descrição:** Retorna todas as atividades de um usuário específico.

**Parâmetros da URL:**
- `id` (obrigatório, string): Identificador do usuário.

**Resposta:**
- `200 OK`: Array de objetos de atividades do usuário.
- `404 Not Found`: Usuário não encontrado.

---

#### 4. Deletar uma Atividade

**Rota:** `DELETE /api/activities/:id`

**Descrição:** Remove uma atividade específica do banco de dados.

**Parâmetros da URL:**
- `id` (obrigatório, string): Identificador da atividade a ser removida.

**Resposta:**
- `200 OK`: Retorna o ID da atividade deletada.
- `404 Not Found`: Atividade não encontrada.

---

#### 5. Deletar Todas as Atividades de um Usuário

**Rota:** `DELETE /api/users/:id/activities`

**Descrição:** Remove todas as atividades associadas a um usuário específico.

**Parâmetros da URL:**
- `id` (obrigatório, string): Identificador do usuário.

**Resposta:**
- `200 OK`: Retorna o ID do usuário e confirma a remoção das atividades.
- `404 Not Found`: Usuário não encontrado.

### Rotas Spotify

Este módulo fornece rotas para integração com a API do Spotify, permitindo interagir com o usuário no Spotify, obter informações sobre a música em reprodução, iniciar e pausar a reprodução de música.

---

#### 1. Obter Dados do Usuário no Spotify

**Rota:** `GET /api/spotify-user`

**Descrição:** Retorna informações básicas do usuário autenticado no Spotify, como ID, nome e imagem.

**Parâmetros da Requisição:**
- **Authorization** (obrigatório): O token de acesso OAuth 2.0 no cabeçalho `Authorization` (formato: `Bearer <token>`).

**Resposta:**
- `200 OK`: Retorna os dados do usuário (id, nome, imagem).
- `401 Unauthorized`: Se o token de acesso não for válido.

---

#### 2. Obter a Música Atualmente Tocando no Spotify

**Rota:** `GET /api/spotify-track`

**Descrição:** Retorna os dados da música que está sendo tocada no momento, incluindo informações como nome da música, artista, duração e imagem do álbum.

**Parâmetros da Requisição:**
- **Authorization** (obrigatório): O token de acesso OAuth 2.0 no cabeçalho `Authorization` (formato: `Bearer <token>`).

**Resposta:**
- `200 OK`: Retorna os dados da música atual (id, nome, artista, duração, imagem do álbum).
- `401 Unauthorized`: Se o token de acesso não for válido.
- `404 Not Found`: Se não houver música tocando no momento.

---

#### 3. Iniciar a Atividade (Iniciar a Reprodução da Música)

**Rota:** `PUT /api/spotify-start`

**Descrição:** Inicia a música no Spotify, colocando o reprodutor no início da música e dando play, caso não esteja tocando.

**Parâmetros da Requisição:**
- **Authorization** (obrigatório): O token de acesso OAuth 2.0 no cabeçalho `Authorization` (formato: `Bearer <token>`).

**Resposta:**
- `200 OK`: Caso a música tenha começado a tocar ou já estivesse tocando.
- `400 Bad Request`: Se a música já estiver tocando no momento.
- `401 Unauthorized`: Se o token de acesso não for válido.
- `500 Internal Server Error`: Se ocorrer um erro ao tentar iniciar a música.

---

#### 4. Pausar a Música (Finalizar a Atividade)

**Rota:** `PUT /api/spotify-pause`

**Descrição:** Pausa a música que está sendo tocada no Spotify.

**Parâmetros da Requisição:**
- **Authorization** (obrigatório): O token de acesso OAuth 2.0 no cabeçalho `Authorization` (formato: `Bearer <token>`).

**Resposta:**
- `200 OK`: Se a música foi pausada com sucesso.
- `204 No Content`: Se a música já estava pausada.
- `401 Unauthorized`: Se o token de acesso não for válido.
- `500 Internal Server Error`: Se ocorrer um erro ao tentar pausar a música.
