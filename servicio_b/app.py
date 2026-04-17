from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/notificar', methods=['POST'])
def notificar():
    datos = request.json
    titulo = datos.get('titulo')
    
    # SIMULACIÓN DE TAREA PESADA (Aquí se queda el time.sleep)
    print(f"Procesando notificación para el ticket: {titulo}...", flush=True)
    time.sleep(7) 
    print("Notificación enviada con éxito al equipo técnico.", flush=True)
    
    return jsonify({"status": "Procesado"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
