import os
import json
from flask import Flask, request
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Cargar credenciales de Google Sheets desde las variables de entorno
# (Configuraremos esto en Render para mayor seguridad)
GOOGLE_CREDENTIALS_JSON = os.environ.get("GOOGLE_CREDENTIALS")

if GOOGLE_CREDENTIALS_JSON:
    cred_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(cred_dict, scopes=scopes)
    gc = gspread.authorize(credentials)
    # Abre la hoja de cálculo por su nombre
    sh = gc.open("Gastos")
    worksheet = sh.sheet1
else:
    worksheet = None

@app.route("/whatsapp", methods=["POST"])
def incoming_message():
    mensaje = request.form.get("Body", "")
    numero_origen = request.form.get("From", "")
    
    if mensaje and worksheet:
        print(f"Gasto recibido: {mensaje}")
        
        ahora = datetime.now()
        fecha = ahora.strftime('%Y-%m-%d')
        hora = ahora.strftime('%H:%M:%S')
        
        # Escribir directamente en Google Sheets
        worksheet.append_row([fecha, hora, mensaje])
        print("Guardado en Google Sheets ✔️")
        
    return "<Response></Response>"

if __name__ == "__main__":
    app.run(port=5000)
