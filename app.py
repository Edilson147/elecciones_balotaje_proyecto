from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os, pymysql
from simulation import run_simulation_from_db, default_params

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-para-flask')

def get_conn():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST','localhost'),
        port=int(os.getenv('MYSQL_PORT','3306')),
        user=os.getenv('MYSQL_USER','root'),
        password=os.getenv('MYSQL_PASSWORD',''),
        database=os.getenv('MYSQL_DB','elecciones2025'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get('/')
def index():
    return render_template('index.html')

@app.post('/enviar')
def enviar():
    data = request.form.to_dict()
    campos = list(data.keys())
    valores = [data[k] for k in campos]

    if not campos:
        return jsonify(ok=False, msg='Formulario vacío'), 400

    cols = ",".join(campos)
    placeholders = ",".join(["%s"]*len(campos))
    sql = f"INSERT INTO encuestas ({cols}) VALUES ({placeholders})"

    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(sql, valores)
        conn.commit()

    return jsonify(ok=True, msg="Respuesta guardada"), 201

@app.route('/simular', methods=['GET','POST'])
def simular():
    params = default_params.copy()
    if request.method == 'POST':
        body = request.get_json(silent=True) or {}
        params.update({k:v for k,v in body.items() if k in params})

    res = run_simulation_from_db(get_conn, **params)
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)
