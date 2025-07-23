from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

# Modelo Pydantic para la solicitud
class AnalysisRequest(BaseModel):
    filename: str
    frame_time: float
    image_base64: str

class ImageAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key='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')
        self.pricing = {
            "gpt-4-turbo": {"input": 0.01/1000, "output": 0.03/1000}
        }
    
    async def analyze_image(self, base64_image: str):
        """Analiza una imagen en base64 con GPT-4 Vision"""
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
            
            return {'analysis': response.choices[0].message.content,
                    'cost': cost
                    }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-image/")
async def analyze_image(request: AnalysisRequest):
    try:
        analyzer = ImageAnalyzer()
        analysis = await analyzer.analyze_image(request.image_base64)
        
        # Guardar comentarios
        with open('comments.txt', 'a', encoding='utf-8') as block:
            block.write('------------------------------------------------------\n')
            block.write(f'nombre del archivo: {request.filename}\n')
            block.write(f'frame analizado: {request.frame_time}\n')
            block.write(f'analisis obtenido: {analysis["analysis"]}\n')
            block.write(f'costo en dolares: {analysis["cost"]}\n')

        return JSONResponse(content={
            "filename": request.filename,
            "frame_time": request.frame_time,
            "analysis": analysis['analysis'],
            "cost": analysis['cost']
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando imagen: {str(e)}")

@app.get("/")
async def health_check():
    return {"status": "API funcionando"}
