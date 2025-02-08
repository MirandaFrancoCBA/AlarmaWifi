from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlitecloud
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Movimiento(BaseModel):
    sensor_id: str
    timestamp: str
    valor: float

def conexion_base_datos():

    api_key = os.getenv("SQLITECLOUD_API_KEY")
    if not api_key:
        raise Exception("API key not found in environment variables.")
    
    conector = sqlitecloud.connect(
        "sqlitecloud://ccmk1asnnk.sqlite.cloud:8860/alarm-database?apikey=" + api_key)
    
    return conector

@app.post("/movimientos/")
def registrar_movimiento(movimiento: Movimiento):
    try:
        conector = conexion_base_datos()
        cursor = conector.cursor()
        cursor.execute(
            "INSERT INTO movimientos (sensor_id, timestamp, valor) VALUES (?, ?, ?)",
            (movimiento.sensor_id, movimiento.timestamp, movimiento.valor),
        )
        conector.commit()
        conector.close()
        return {"status": "Movimiento registrado"}
    
    except Exception as e:
        print(f"Error al registrar movimiento: {str(e)}")  # Log del error completo
        raise HTTPException(status_code=500, detail=f"Error al registrar movimiento: {str(e)}")

@app.get("/movimientos/")
def obtener_movimientos():
    try:
        conector = conexion_base_datos()
        movimientos = conector.execute("SELECT * FROM movimientos").fetchall()
        conector.close()
        return [dict(movimiento) for movimiento in movimientos]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener movimientos: {str(e)}")