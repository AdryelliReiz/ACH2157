async function webAppRoutes(fastify, options) {
    //=====================<Rotas da paǵina Web>=====================
  
    fastify.get('/', async (request, reply) => {
        return reply.sendFile('index.html');
    });

    fastify.get('/profile', async (request, reply) => {
        return reply.sendFile('profile.html');
    });

    fastify.get('/activity', async (request, reply) => {
        return reply.sendFile('activity.html');
    });
  
}
  
module.exports = webAppRoutes;
  