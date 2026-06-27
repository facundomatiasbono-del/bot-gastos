import os
import json
from flask import Flask, request
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Nombre exacto de tu archivo JSON subido a GitHub
JSON_FILE = "level-landing-500703-q7-0cffdb7755f1.json"

if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        cred_dict = json.load(f)
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(cred_dict, scopes=scopes)
    gc = gspread.authorize(credentials)
    # Abre la hoja de cálculo por su nombre ("Gastos")
    sh = gc.open("Gastos")
    worksheet = sh.sheet1
else:
    worksheet = None
    print(f"⚠️ Advertencia: No se encuentra el archivo {JSON_FILE}")

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
