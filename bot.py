from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def incoming_message():
    # Obtenemos el texto del mensaje que enviaste por WhatsApp
    mensaje = request.form.get("Body", "")
    numero_origen = request.form.get("From", "")
    
    if mensaje:
        print(f"Gasto recibido: {mensaje}")
        
        # Guardamos en el CSV local
        ahora = datetime.now()
        with open("gastos.csv", "a", encoding="utf-8") as archivo:
            archivo.write(f"{ahora.strftime('%Y-%m-%d')},{ahora.strftime('%H:%M:%S')},{mensaje}\n")
            
        print("Guardado en gastos.csv ✔️")
        
    return "<Response></Response>"

if __name__ == "__main__":
    app.run(port=5000)