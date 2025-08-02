from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime

load_dotenv()

app = FastAPI()

COMMENTS_FILE = Path("comments.txt")
COMMENTS_FILE.touch(exist_ok=True)

class AnalysisRequest(BaseModel):
    filename: str
    capture_time: str  # Cambiado de float (frame_time) a str para la hora exacta
    image_base64: str

class ImageAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.pricing = {
            "gpt-4-turbo": {"input": 0.01/1000, "output": 0.03/1000}
        }
    
    async def analyze_image(self, base64_image: str):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Analiza el contenido de esta imagen de video."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe los elementos principales en esta imagen:"},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ],
                max_tokens=300
            )

            pricing = self.pricing.get(response.model, self.pricing["gpt-4-turbo"])
            cost = (response.usage.prompt_tokens * pricing["input"] + 
                    response.usage.completion_tokens * pricing["output"])
            
            return {
                'analysis': response.choices[0].message.content,
                'cost': cost
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-image/")
async def analyze_image(request: AnalysisRequest):
    try:
        analyzer = ImageAnalyzer()
        analysis = await analyzer.analyze_image(request.image_base64)
        
        try:
            with open(COMMENTS_FILE, 'a', encoding='utf-8') as f:
                f.write(f"""
Archivo: {request.filename}
Hora de captura: {request.capture_time}
Análisis: {analysis['analysis']}
Costo: ${analysis['cost']:.6f}
\n""")
                f.flush()
        except IOError as e:
            print(f"Error escribiendo en archivo: {e}")

        return JSONResponse(content={
            "filename": request.filename,
            "capture_time": request.capture_time,  # Cambiado de frame_time
            "analysis": analysis['analysis'],
            "cost": analysis['cost']
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando imagen: {str(e)}")

@app.get("/comments/", response_class=PlainTextResponse)
async def view_comments():
    try:
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "No hay comentarios registrados"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {"status": "API funcionando"}
