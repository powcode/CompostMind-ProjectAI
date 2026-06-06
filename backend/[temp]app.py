from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io

try:
    from logic import logic_compos
    print("File logic.py berhasil disambungkan!")
except ImportError:
    print("File logic.py ditemukan, tapi fungsi 'hitung_kompos' belum ada atau berbeda nama.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

try:
    model = YOLO("best.pt")
    print("🔥 Otak AI YOLO Berhasil Dimuat!")
except Exception as e:
    print(f"❌ Gagal memuat file best.pt. Pastikan file 'best.pt' sudah kamu copas ke folder yang sama! Error: {e}")

@app.post("/api/scan-kompos")
async def scan_komposisi(file: UploadFile = File(...)):
    try:
  
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        results = model(image)

        detected_labels = []
        highest_conf = 0
        main_item_name = "Tidak Terdeteksi"

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label_name = model.names[class_id]
                detected_labels.append(label_name)

                conf_score = float(box.conf[0]) * 100
                if conf_score > highest_conf:
                    highest_conf = round(conf_score, 1)
                    main_item_name = label_name

        
        if detected_labels and highest_conf >= 60.0:
            status_kompos = logic_compos(detected_labels)
        else:
            main_item_name = "Tidak Terdeteksi"
            highest_conf = 0.0
            status_kompos = {
                "bisa_dikompos" : False,
                "status": "Tidak Terdeteksi",
                "solusi": "Pastikan objek sampah terlihat jelas"
            }

        return {
           "status": "success",
            "isCompostable": status_kompos["bisa_dikompos"],
            "itemName": main_item_name.capitalize(),
            "confidence": highest_conf if highest_conf > 0 else 0,
            "detected_objects": detected_labels,
            "kesimpulan_logika": status_kompos
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}