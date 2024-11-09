async function userRoutes(fastify, options) {
    const db = fastify.db;

    //=====================<Rotas de Usuários>=====================
  
    // Rota para adicionar um novo usuário
    fastify.post('/api/users', async (request, reply) => {
        const { id, name } = request.body;
        if (!id || !name) {
            return reply.status(400).send({ error: 'Id and Name are required' });
        }

        // Verifica se o usuário já existe
        const user = await db.prepare('SELECT * FROM users WHERE id = ?').get(id);

        if (user) {
            // Pega todas as atividades do usuário
            const activities = await db.prepare('SELECT * FROM activities WHERE userId = ?').all(id);

            user.activities = activities.length;
            // Calcula a duração total das atividades
            user.totalDuration = activities.length > 0 
                ? activities.reduce((acc, activity) => acc + activity.duration, 0)
                : 0;
            // Calcula o total de calorias queimadas 
            user.caloriesBurned = activities.length > 0
                ? activities.reduce((acc, activity) => acc + activity.caloriesBurned, 0)
                : 0;
            reply.send(user);
        }
  
        const result = await db.prepare('INSERT INTO users (id, name) VALUES (?, ?)').run(id,name);
        reply.send({ id: result.lastInsertRowid, name, weight: null, activities: 0, totalDuration: 0, caloriesBurned: 0 });
    });
  
    // Rota para listar todos os usuários
    fastify.get('/api/users', async (request, reply) => {
        const users = await db.prepare('SELECT * FROM users').all();
        reply.send(users);
    });
  
    // Rota para obter um usuário específico pelo ID
    fastify.get('/api/users/:id', async (request, reply) => {
        const user = await db.prepare('SELECT * FROM users WHERE id = ?').get(request.params.id);
    
        if (!user) {
            return reply.status(404).send({ error: 'User not found' });
        }

        // Busca todas as atividades do usuário
        const activities = await db.prepare('SELECT * FROM activities WHERE userId = ?').all(request.params.id);

        user.activities = activities.length;
        // Calcula a duração total das atividades
        user.totalDuration = activities.length > 0 
            ? activities.reduce((acc, activity) => acc + activity.duration, 0)
            : 0;

        // Calcula o total de calorias queimadas
        user.caloriesBurned = activities.length > 0
            ? activities.reduce((acc, activity) => acc + activity.caloriesBurned, 0)
            : 0;
        reply.send(user);
    });

    // Rota para atualizar o peso do usuário
    fastify.put('/api/users/:id', async (request, reply) => {
        const { weight } = request.body;
        if (!weight) {
            return reply.status(400).send({ error: 'Weight is required' });
        }
    
        const result = await db.prepare('UPDATE users SET weight = ? WHERE id = ?').run(weight, request.params.id);
        if (result.changes === 0) {
            return reply.status(404).send({ error: 'User not found' });
        }
    
        reply.status(204).send();
    });

    // Rota para deletar um usuário
    fastify.delete('/api/users/:id', async (request, reply) => {
        const result = await db.prepare('DELETE FROM users WHERE id = ?').run(request.params.id);
    
        if (result.changes === 0) {
            return reply.status(404).send({ error: 'User not found' });
        }

        // Deleta todas as atividades do usuário
        await db.prepare('DELETE FROM activities WHERE userId = ?').run(request.params.id);
    
        reply.send({ id: request.params.id });
    });
}
  
module.exports = userRoutes;
  