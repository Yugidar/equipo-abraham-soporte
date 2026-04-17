from flask import Flask, request, jsonify, render_template_string
import mysql.connector
import os
import requests # Para hablar con el Servicio B

app = Flask(__name__)

# Conexión a RDS usando variables de entorno
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME')
    )

HTML_FORM = """
<!DOCTYPE html><html><body>
<h2>Soporte Técnico - Registro de Ticket</h2>
<form method="POST" action="/abrir_ticket">
    Título: <input name="titulo" required><br>
    Prioridad: <select name="prioridad">
        <option value="Baja">Baja</option>
        <option value="Media">Media</option>
        <option value="Alta">Alta</option>
    </select><br>
    ID Cliente: <input name="id_cliente" type="number" required><br>
    <input type="submit" value="Enviar Ticket">
</form>
<br><a href="/tickets">Ver Tickets Abiertos</a>
</body></html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/abrir_ticket', methods=['POST'])
def abrir_ticket():
    try:
        titulo = request.form.get('titulo')
        prio = request.form.get('prioridad')
        cliente = request.form.get('id_cliente')

        # 1. Guardar en RDS (Operación rápida)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tickets (titulo, prioridad, id_cliente) VALUES (%s, %s, %s)", (titulo, prio, cliente))
        conn.commit()
        conn.close()

        # 2. Notificar al Servicio B (Delegar la tarea pesada)
        status_b = ""
        try:
            # IMPORTANTE: Usamos el nombre del servicio en Docker como hostname
            requests.post('http://servicio_b:5001/notificar', json={"titulo": titulo})
            status_b = "Notificación enviada al área técnica."
        except:
            status_b = "Servicio de notificaciones en mantenimiento. Ticket guardado."

        return jsonify({"mensaje": "Ticket abierto", "notificacion": status_b}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tickets', methods=['GET'])
def listar():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets ORDER BY FIELD(prioridad, 'Alta', 'Media', 'Baja')")
    tickets = cursor.fetchall()
    conn.close()
    return jsonify(tickets)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
