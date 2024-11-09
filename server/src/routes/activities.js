async function activityRoutes(fastify, options) {
    const db = fastify.db;

    //=====================<Rotas de Atividades>=====================

    // Rotas para registrar uma atividade
    fastify.post('/api/activities', async (request, reply) => {
        const { userId, musicId, duration, date } = request.body;
        if (!userId || !musicId || !duration || !date) {
            return reply.status(400).send({ error: 'userId, musicId, duration and date are required' });
        }

        // Verifica se o usuário existe
        const user = await db.prepare('SELECT * FROM users WHERE id = ?').get(userId);

        if (!user) {
            return reply.status(404).send({ error: 'User not found' });
        }

        const caloriesBurned = 4.5 * user.weight * (duration / 60);
    
        const result = await db.prepare('INSERT INTO activities (userId, musicId, duration, caloriesBurned, date) VALUES (?, ?, ?, ?, ?)').run(userId, musicId, duration, caloriesBurned, date);
        reply.send({ id: result.lastID, userId, musicId, duration, date });
    });

    // Rota para listar todas as atividades
    fastify.get('/api/activities', async (request, reply) => {
        const activities = await db.prepare('SELECT * FROM activities').all();
        reply.send(activities);
    });

    // Rota para listar todas as atividades de um usuário
    fastify.get('/api/users/:id/activities', async (request, reply) => {
        // Verifica se o usuário existe
        const user = await db.prepare('SELECT * FROM users WHERE id = ?').get(request.params.id);

        if (!user) {
            return reply.status(404).send({ error: 'User not found' });
        }

        const activities = await db.prepare('SELECT * FROM activities WHERE userId = ?').all(request.params.id);
        reply.send(activities);
    });

    // Rota para deletar uma atividade
    fastify.delete('/api/activities/:id', async (request, reply) => {
        const result = await db.prepare('DELETE FROM activities WHERE id = ?').run(request.params.id);

        if (result.changes === 0) {
            return reply.status(404).send({ error: 'Activity not found' });
        }
    
        reply.send({ id: request.params.id });
    });

    // Rota para deletar todas as atividades de um usuário
    fastify.delete('/api/users/:id/activities', async (request, reply) => {
        // Verifica se o usuário existe
        const user = await db.prepare('SELECT * FROM users WHERE id = ?').get(request.params.id);

        if (!user) {
            return reply.status(404).send({ error: 'User not found' });
        }

        await db.prepare('DELETE FROM activities WHERE userId = ?').run(request.params.id);
        reply.send({ userId: request.params.id });
    });
}
  
module.exports = activityRoutes;
  