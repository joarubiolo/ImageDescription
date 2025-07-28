import cv2
import time
import os
import requests
import base64
import json

# Inicializar la cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

url = "https://imagedetection-zatek.onrender.com/analyze-image/"
frame_interval = float(input("Ingresa el intervalo entre frames (segundos): "))  # Cambiado de frame_time a frame_interval
current_time = 0.0  # Tiempo acumulado para cada frame
photo_count = 0
auto_capture = False
last_capture = time.time()
photo_files = []
encoded_images = []

print('Modos:\n"f" - Foto manual\n"e" - Activar/desactivar captura automática\n"q" - Salir')

def send_to_server(filename, current_time, image_base64):
    payload = {
        "filename": filename,
        "frame_time": current_time,  # Usamos el tiempo acumulado
        "image_base64": image_base64
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            print(f"\nRespuesta del servidor para {filename}:")
            print(f"Tiempo del frame: {current_time}s")
            print(f"Tamaño enviado: {len(image_base64)/1024:.2f} KB")
            print("Resultado:", response.json())
        else:
            print(f"Error en la respuesta (Código {response.status_code}): {response.text}")
        return True
    except Exception as e:
        print(f"Error al enviar {filename}: {str(e)}")
        return False

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("No se pudo recibir el frame. Saliendo...")
        break
    
    cv2.imshow('Webcam - Modos: f=foto, e=auto, q=salir', frame)
    
    if auto_capture and (time.time() - last_capture >= frame_interval):
        photo_name = f'auto_foto_{photo_count}.jpg'
        cv2.imwrite(photo_name, frame)
        
        _, buffer = cv2.imencode('.jpg', frame)
        base64_image = base64.b64encode(buffer).decode('utf-8')
        
        if send_to_server(photo_name, current_time, base64_image):
            photo_files.append(photo_name)
            encoded_images.append(base64_image)
            photo_count += 1
            last_capture = time.time()
            current_time += frame_interval  # Incrementamos el tiempo acumulado
            
            cv2.putText(frame, 'Foto enviada!', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Webcam - Modos: f=foto, e=auto, q=salir', frame)
            cv2.waitKey(300)
        else:
            os.remove(photo_name)
    
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break
    elif key == ord('f'):
        photo_name = f'foto_manual_{photo_count}.jpg'
        cv2.imwrite(photo_name, frame)
        
        _, buffer = cv2.imencode('.jpg', frame)
        base64_image = base64.b64encode(buffer).decode('utf-8')
        
        if send_to_server(photo_name, current_time, base64_image):
            photo_files.append(photo_name)
            encoded_images.append(base64_image)
            photo_count += 1
            current_time += frame_interval
            
            cv2.putText(frame, 'Foto enviada!', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Webcam - Modos: f=foto, e=auto, q=salir', frame)
            cv2.waitKey(500)
        else:
            os.remove(photo_name)
    elif key == ord('e'):
        auto_capture = not auto_capture
        status = "ACTIVADA" if auto_capture else "DESACTIVADA"
        print(f'Captura automática {status}')
        last_capture = time.time()

if photo_files:
    delete = input(f"\n¿Deseas borrar las {len(photo_files)} capturas locales? [s/n]: ").lower()
    if delete == 's':
        print("Borrando capturas...")
        for file in photo_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"Borrado: {file}")
else:
    print("\nNo hay capturas para borrar.")

cap.release()
cv2.destroyAllWindows()
