from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import cv2
import os
import shutil

app = FastAPI()

# --- Autoriser React (localhost) à accéder à l'API ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dans un projet réel, remplacer par l'URL front
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dossiers de stockage ---
UPLOAD_DIR = "videos"             # Vidéos uploadées
FRAMES_DIR = os.path.join(UPLOAD_DIR, "frames")  # Frames extraites
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)

# --- Servir les frames en statique ---
app.mount("/frames", StaticFiles(directory=FRAMES_DIR), name="frames")

# --- Endpoint test santé ---
@app.get("/")
def health_check():
    return {"status": "ok"}

# --- Endpoint principal pour analyser la vidéo ---
@app.post("/analyze")
def analyze_video(file: UploadFile = File(...)):
    """
    Étapes :
    1. Sauvegarder la vidéo uploadée dans UPLOAD_DIR
    2. Lire la vidéo avec OpenCV
    3. Pour chaque seconde :
       - Extraire une frame
       - Calculer la luminosité moyenne
       - Sauvegarder la frame en .jpg
    4. Retourner un JSON avec frames + luminosité
    """
    video_path = os.path.join(UPLOAD_DIR, file.filename)

    # 1️⃣ Sauvegarde de la vidéo
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2️⃣ Lecture avec OpenCV
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames par seconde

    results = []
    frame_index = 0
    second = 0

    # 3️⃣ Parcourir toutes les frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Prendre 1 frame par seconde
        if fps > 0 and int(frame_index % fps) == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Conversion en gris
            brightness = gray.mean()  # Luminosité moyenne

            # 3️⃣ Sauvegarde de la frame
            frame_filename = f"{os.path.splitext(file.filename)[0]}_frame_{second}.jpg"
            frame_path = os.path.join(FRAMES_DIR, frame_filename)
            cv2.imwrite(frame_path, frame)

            # Ajouter au résultat JSON
            results.append({
                "second": second,
                "brightness": round(float(brightness), 2),
                "frame_url": f"/frames/{frame_filename}"
            })
            second += 1

        frame_index += 1

    cap.release()

    # 4️⃣ Retour JSON pour React
    return {
        "frames_analyzed": len(results),
        "results": results
    }
