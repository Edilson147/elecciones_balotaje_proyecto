# Proyecto: Encuesta + Simulación de Elecciones (1ra y Balotaje)

## Requisitos
- Python 3.10+
- pip install -r requirements.txt
- MySQL 8.x (o MariaDB)

## Variables de entorno
Crea un archivo `.env` con:
```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_password
MYSQL_DB=elecciones2025
SECRET_KEY=dev-key-para-flask
```

## Pasos
1. Crear BD y tabla:
   ```bash
   mysql -u tu_usuario -p -e "CREATE DATABASE IF NOT EXISTS elecciones2025 CHARACTER SET utf8mb4;"
   mysql -u tu_usuario -p elecciones2025 < schema.sql
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar servidor:
   ```bash
   python app.py
   ```
4. Formularios:
   - Abrir http://localhost:5000/ (página estática + formulario).
   - Enviar respuestas; se guardan en MySQL.
5. Simulación:
   - GET `http://localhost:5000/simular` devuelve JSON con probabilidades del balotaje.
   - POST `/simular` con JSON para cambiar parámetros (n_trials, margen_error, p_indecisos_a/b).
# elecciones_balotaje_proyecto
