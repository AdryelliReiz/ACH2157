const fastifyPlugin = require('fastify-plugin');
const path = require('path');
const Database = require('better-sqlite3');

async function sqlitePlugin(fastify, options) {
const db = new Database(path.join(__dirname, '../../database/database.sqlite'), { verbose: console.log });

  // Decorate Fastify with the SQLite database connection
  fastify.decorate('db', db);

  // Criar tabela no banco de dados, se não existir
  db.prepare(`
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        weight REAL
    );
  `).run();

  db.prepare(`
     CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userId INTEGER NOT NULL,
        musicId TEXT NOT NULL,
        duration INTEGER NOT NULL,
        caloriesBurned REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (userId) REFERENCES users(id)
    )`).run();
}

module.exports = fastifyPlugin(sqlitePlugin);
