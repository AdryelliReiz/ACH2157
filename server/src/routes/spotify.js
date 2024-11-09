const axios = require('axios');

async function spotifyRoutes(fastify, options) {
    //=====================<Rotas do SPotify>=====================

    // Rota para obter dados do usuário no Spotify
    fastify.get('/api/spotify-user', async (request, reply) => {
        const response = await axios.get('https://api.spotify.com/v1/me', {
            headers: {
                Authorization: `Bearer ${request.headers.authorization.replace('Bearer ', '')}`
            }
        });

        if (response.status == 200) {
            const data = {
                id: response.data.id,
                name: response.data.display_name,
                image_url: response.data.images[0].url
            }
            reply.send(data);
        } else {
            reply.status(401).send({ message: "Não autorizado" });
        }
        
    });

    fastify.get('/api/spotify-track', async (request, reply) => {
        // Busca a música que está sendo tocada no Spotify agora
        const response = await axios.get('https://api.spotify.com/v1/me/player/currently-playing', {
            headers: {
                Authorization: `Bearer ${request.headers.authorization.replace('Bearer ', '')}`
            }
        });

        if(response.status == 200) {
            // Pega os dados da música
            const data = {
                id: response.data.item.id,
                name: response.data.item.name,
                artist: response.data.item.artists[0].name,
                duration: response.data.item.duration_ms,
                album_img: response.data.item.album.images[0].url
            }

            reply.send(data);

        } else {
            reply.status(response.status).send(response.data);
        }
    });

    // Rota para iniciar a atividade tocando uma música
    fastify.put('/api/spotify-start', async (request, reply) => {
        const accessToken = request.headers.authorization.replace('Bearer ', '');
    
        // Tenta realizar o `seek` para o início da música
        const responseSeek = await axios.put('https://api.spotify.com/v1/me/player/seek?position_ms=0', null, {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        });
    
        // Checa o status da resposta do `seek`
        if (responseSeek.status !== 200) {
            return reply.status(responseSeek.status).send(responseSeek.data);
        }

        // Vefifica se a música está pausada
        const responseSong = await axios.get('https://api.spotify.com/v1/me/player/currently-playing', {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        });

        if(responseSong.status == 200 && responseSong.data.is_playing) {
            return reply.status(200).send({ message: "A música já está tocando" });
        }
    
        // Tenta dar play na música
        await axios.put('https://api.spotify.com/v1/me/player/play', null, {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        });
    
        // Responde ao cliente se o `play` foi bem-sucedido
        reply.status(200).send();
    });

    // Finalizar a atividade pausando a música
    fastify.put('/api/spotify-pause', async (request, reply) => {
        const response = await axios.put('https://api.spotify.com/v1/me/player/pause', null, {
            headers: {
                Authorization: `Bearer ${request.headers.authorization.replace('Bearer ', '')}`
            }
        });

        if(response.status == 204 || response.status == 200) {
            reply.send();
        } else {
            reply.status(response.status).send(response.data);
        }
    });
}
  
module.exports = spotifyRoutes;
  