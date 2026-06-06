from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import cv2
import numpy as np
import sys
import os

# Tambahkan path backend ke sys.path agar bisa import logic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from logic import logic_compos

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model dari direktori backend
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best.pt")
model = YOLO(model_path) # Otak YOLOv8 kamu

# ENDPOINT 1: Khusus untuk Live Scanning Interval Per Detik (QRIS Mode)
@app.post("/api/check-object")
async def check_object(file: UploadFile = File(...)):
    try:
        # Baca file image stream yang dikirim JavaScript
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Jalankan prediksi YOLO kilat
        results = model(frame, verbose=False)
        
        is_found = False
        detected_name = ""
        
        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                # Jika akurasi di atas 65%, kunci status objek ditemukan!
                if conf >= 0.65:
                    class_id = int(box.cls[0])
                    detected_name = model.names[class_id]
                    is_found = True
                    break
                    
        return {
            "is_object_found": is_found,
            "item_name": detected_name
        }
    except Exception as e:
        return {"is_object_found": False, "message": str(e)}

# ENDPOINT 2: Endpoint Utama Kamu (Memicu YOLO + Gemini AI Logic)
@app.post("/api/scan-kompos")
async def scan_kompos(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        results = model(frame, verbose=False)
        detected_labels = []
        best_confidence = 0.0
        best_label = "Unknown item"

        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                class_id = int(box.cls[0])
                label = model.names.get(class_id, str(class_id))
                detected_labels.append(label)
                if conf > best_confidence:
                    best_confidence = conf
                    best_label = label

        logic_result = logic_compos(detected_labels)

        return {
            "status": "success",
            "itemName": best_label,
            "confidence": round(best_confidence * 100, 2),
            "isCompostable": bool(logic_result.get("bisa_dikompos", False)),
            "kesimpulan_logika": logic_result,
            "detections": detected_labels,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
