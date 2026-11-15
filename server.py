from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
from bs4 import BeautifulSoup
from google import genai

app = FastAPI()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class Prospecto(BaseModel):
    url: str

@app.post("/analizar")
def analizar(datos: Prospecto):
    try:
        response = requests.get(datos.url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        texto_web = " ".join([p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3'])])[:5000]

        prompt = f"""
        Actúa como un experto en ventas B2B y asesor comercial de nuestra agencia. 
        Analiza esta empresa según su web, califica sus puntos débiles y genera una estrategia de ventas y correo en frío:
        URL: {datos.url}
        Contenido: {texto_web}
        """
        
        response_ai = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )
        return {"exito": True, "analisis": response_ai.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
