import asyncpg

async def connect_to_db(app):
    """Conecta a la base de datos usando la configuración de Flask."""
    conn = await asyncpg.connect(
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_NAME'],
        host=app.config['DB_HOST'],
        port=app.config['DB_PORT']
    )
    return conn

async def init_db(app):
    """Inicializa la conexión a la base de datos y verifica la versión."""
    conn = await connect_to_db(app)
    version = await conn.fetch("SELECT version();")
    print(f"Conectado a la base de datos. Versión: {version[0]['version']}")
    await conn.close()
