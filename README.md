# Sistema de Análisis de Imágenes en Tiempo Real
Este proyecto es un sistema que permite capturar imágenes desde una cámara web, enviarlas a un servidor para su análisis mediante inteligencia artificial (usando el modelo GPT-4 Vision de OpenAI), y almacenar los resultados en un archivo de texto. Está compuesto por dos partes principales: un cliente que captura las imágenes y un servidor que las procesa.
----------
## Características principales
- **Captura de imágenes**: Toma fotos manualmente o automáticamente a intervalos regulares.
- **Análisis con IA**: Utiliza el modelo de OpenAI para describir el contenido de las imágenes.
- **Registro de resultados**: Guarda los análisis en un archivo de texto con formato claro.
- **Interfaz sencilla**: El cliente muestra una ventana con la cámara y responde a comandos del teclado.
## Ventajas
- **Automatización**: Permite la captura automática de imágenes sin intervención.
- **Eficiencia**: Optimiza el uso de la IA al enviar solo las imágenes necesarias.
- **Registro persistente**: Los análisis se guardan en un archivo para consulta posterior.
- **Flexibilidad**: Se puede usar tanto en modo manual como automático.
## Requisitos de hardware
- **Cámara web**: Funcional y accesible por el sistema.
- **Conexión a Internet**: Necesaria para enviar las imágenes al servidor y usar la API de OpenAI.
- **Procesador y memoria**: Dependerá del volumen de imágenes, pero se recomienda un sistema con al menos 4GB de RAM y un procesador moderno.
## Requisitos de software
- Python 3.7 o superior
- Dependencias listadas en `requirements.txt`
## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura las variables de entorno:
   - Crea un archivo `.env` en la raíz del proyecto del servidor con tu API key de OpenAI:
     ```
     OPENAI_API_KEY=tu_api_key
     ```
## Uso
### Servidor (FastAPI)
1. Navega al directorio del servidor (si está separado).
2. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```
   El servidor estará disponible en `http://localhost:8000`.
### Cliente (Captura de imágenes)
1. Ejecuta el script del cliente:
   ```bash
   python cliente_camara.py
   ```
2. Sigue las instrucciones:
   - Ingresa el intervalo de tiempo (en segundos) entre capturas automáticas.
   - Usa los comandos:
     - `f`: Toma una foto manualmente.
     - `e`: Activa/desactiva la captura automática.
     - `q`: Sale del programa.
3. Las imágenes capturadas se envían al servidor y los análisis se guardan en `comments.txt`.
## Consideraciones
- **Tiempos de respuesta del servidor**: El análisis de imágenes puede demorar varios segundos dependiendo de la carga de OpenAI y la velocidad de Internet.
- **Costos de la API de OpenAI**: Cada análisis tiene un costo asociado. Monitorea tu uso para evitar gastos inesperados.
- **Seguridad**: El servidor está diseñado para desarrollo. Para producción, implementa HTTPS y autenticación.
- **Almacenamiento**: Las imágenes capturadas se guardan temporalmente en el cliente y se borran al final, pero los análisis persisten en el servidor.
## Estructura del proyecto
```
proyecto/
│
├── cliente_camara.py       # Script para capturar imágenes
├── main.py                 # Servidor FastAPI
├── requirements.txt        # Dependencias
├── .env                    # Variables de entorno (crear manualmente)
└── comments.txt            # Resultados de los análisis (generado automáticamente)
```
## Ejemplo de funcionamiento
### Cliente
![Ventana del cliente mostrando la cámara y el mensaje "Foto enviada!"](cliente.png) *(Imagen de ejemplo: captura de pantalla de la ventana del cliente)*
### Servidor
El servidor responde con un JSON que incluye el análisis y el costo. Además, los análisis se acumulan en `comments.txt`:
```
Archivo: auto_foto_0.jpg
Tiempo: 10.0s
Análisis: La imagen muestra a un hombre joven sentado frente a una computadora...
Costo: $0.009160
Archivo: auto_foto_1.jpg
Tiempo: 20.0s
Análisis: En esta imagen se ve a la misma persona levantando las manos...
Costo: $0.008680
```
### Visualización de comentarios
Para ver los comentarios, visita `http://localhost:8000/comments/` en tu navegador.
✅🕒ℹ️💡
