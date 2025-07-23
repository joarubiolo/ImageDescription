# 🎥 Analizador de Videos con Inteligencia Artificial

**Sistema inteligente que extrae y analiza fotogramas específicos de videos usando GPT-4 Vision de OpenAI**

## 🌟 Características principales

- Extrae fotogramas exactos de videos en el momento que elijas
- Genera descripciones detalladas del contenido visual usando IA
- Registra historial de análisis con costos y descripciones
- Procesamiento local de videos (más rápido y privado)

## ⚙️ ¿Cómo funciona?

### Flujo del sistema
1. **Extracción**: Captura un fotograma exacto de tu video en el segundo que indiques
2. **Codificación**: Convierte la imagen a formato base64 (texto seguro para internet)
3. **Análisis**: Envía la imagen a la IA de OpenAI para su interpretación
4. **Resultados**: Devuelve una descripción en lenguaje natural de lo que aparece

### Componentes clave
- **Cliente**: Procesa el video localmente en tu computadora
- **Servidor**: Se comunica con la IA de OpenAI
- **Base64**: "Traductor" que convierte imágenes a texto para enviarlas por internet

## 📋 Guía de uso

### Requisitos
- Python 3.8 o superior
- Clave API de OpenAI (en archivo `.env`)
- Paquetes necesarios: `fastapi`, `openai`, `python-dotenv`, `opencv-python`, `requests`

### Instalación
1. Clona este repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución
1. Inicia el servidor:
   ```bash
   uvicorn fastapi_app:app --reload
   ```
2. Ejecuta el cliente:
   ```bash
   python test.py
   ```
3. Sigue las instrucciones para:
   - Ingresar la ruta de tu video
   - Especificar el segundo a analizar

### Ejemplo de resultado
```
Respuesta del servidor:
{
  "nombre_archivo": "ejemplo.mp4",
  "tiempo_analizado": 5.0,
  "analisis": "La imagen muestra un golden retriever jugando en un parque...",
  "costo": 0.0023
}
```

## 📊 Historial de análisis
Todos los análisis se guardan automáticamente en `comments.txt` con:
- Nombre del archivo
- Segundo analizado
- Descripción generada
- Costo del análisis

## 💡 Usos prácticos
- Revisión de cámaras de seguridad
- Análisis de jugadas deportivas
- Educación con videos explicativos
- Monitoreo de mascotas
- Moderación de contenido

## ⚠️ Limitaciones
- Formatos soportados: MP4, MOV, AVI
- Duración máxima recomendada: 30 minutos
- La precisión depende de la calidad del video y de OpenAI
