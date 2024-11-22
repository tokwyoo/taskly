# Archivo exclusivo para desarrollo.  
# Ejecuta la aplicación Flask con el servidor integrado.  
# No usar en producción.  

from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
