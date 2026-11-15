from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

class Prospecto(BaseModel):
    url: str

@app.post("/analizar")
def analizar(datos: Prospecto):
    try:
        resultado = subprocess.run(
            ["python", "scripts/analyze_prospect.py", datos.url],
            capture_output=True,
            text=True,
            check=True
        )
        return {"exito": True, "analisis": resultado.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr)
