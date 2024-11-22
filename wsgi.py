# Archivo de entrada para producción.  
# Diseñado para usarse con un servidor WSGI como Gunicorn.  

from app import create_app

app = create_app()
