from app import app
from flask import render_template
import sqlite3
from datetime import datetime

def obtener_movimientos():
    # Conectar a la base de datos (ajustar la ruta de la base de datos)
    con = sqlite3.connect('movimientos.db')  # Ajusta según la ubicación de tu base de datos
    cur = con.cursor()
    cur.execute("SELECT timestamp FROM movimientos")
    movimientos = cur.fetchall()
    con.close()
    return movimientos

def clasificar_movimientos(movimientos):
    # Contar movimientos durante el día y la noche
    day_count = 0
    night_count = 0
    for movimiento in movimientos:
        timestamp = movimiento[0]
        hora = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").hour
        
        if 6 <= hora < 18:  # Día de 6 AM a 6 PM
            day_count += 1
        else:  # Noche de 6 PM a 6 AM
            night_count += 1
    
    return day_count, night_count

@app.route('/')
def index():
    movimientos = obtener_movimientos()
    day_count, night_count = clasificar_movimientos(movimientos)
    
    return render_template('index.html', day_count=day_count, night_count=night_count)