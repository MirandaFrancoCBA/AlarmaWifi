from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlitecloud

app = FastAPI()

class Movimiento(BaseModel):

    sensor_id: str
    timestamp: str
    valor: float

def conexion_base_datos():
    conector = sqlitecloud.connect(
        url="sqlitecloud://ccmk1asnnk.sqlite.cloud:8860/alarm-database?apikey=vIawZmLuIcyTnWDxRhbQ0aNFQGUtBXM4abWk8KvJgbw",
        api_key="<admin_apikey>"
    )
    #conector.row_factory = sqlite3.Row
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
