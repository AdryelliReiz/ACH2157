const fastify = require('fastify')({ logger: true });
const sqlitePlugin = require('./plugins/sqlite');;
const path = require('path');

// Registrar o plugin de SQLite
fastify.register(sqlitePlugin);

// Configuração do CORS
fastify.register(require('@fastify/cors'), {
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization']
});

fastify.register(require('@fastify/static'), {
    root: path.join(__dirname, '..', 'public'),
    prefix: '/', 
});

// Registra as rotas
fastify.register(require('./routes/users'));
fastify.register(require('./routes/activities'));
fastify.register(require('./routes/spotify'));
fastify.register(require('./routes/webApp'));

// Inicia o servidor
const start = async () => {
  try {
    await fastify.listen({ port: 8080 });
    console.log('Servidor iniciado no endereço => http://localhost:8080');
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
