import os
from google import genai
from google.genai import types

# Inisialisasi Client Gemini API
try:
    pass
    # client = genai.Client()
except Exception as e:
    print(f"⚠️ Warning: Gemini Client gagal dimuat. Error: {e}")
    client = None

def generate_gemini_response(nama_objek, bisa_dikompos):
    """
    Fungsi untuk meminta Gemini API membuat teks edukasi pendek
    berdasarkan System Prompt buatanmu.
    """
    if not client:
        return "Asisten AI tidak siap (API Key belum dikonfigurasi)."

    # --- DISINI SYSTEM PROMPT KAMU DIMASUKKAN secra terstruktur ---
    system_instruction = """
    Kamu adalah seorang "Asisten Kompos Cerdas" (Compost Mind Agent) yang bertugas memberikan feedback instan, edukatif, dan ramah berdasarkan objek yang dideteksi oleh kamera pengguna (menggunakan model YOLO Object Detection).

    Tugas utama kamu adalah menerima input berupa NAMA OBJEK yang dideteksi, lalu menghasilkan output teks pendek (maksimal 2-3 kalimat) dengan aturan berikut:

    KATEGORI 1: OBJEK DAPAT DIKOMPOSKAN (COMPOSABLE - ORGANIK)
    Jika objek yang dideteksi adalah bahan organik (seperti: kulit pisang, daun kering, sisa sayur, cangkang telur, ampas kopi, dll), berikan:
    1. Kata-kata pujian atau apresiasi di awal karena pengguna memilih bahan yang tepat.
    2. Penjelasan singkat dalam waktu singkat tentang manfaat spesifik bahan tersebut untuk kompos (misalnya kandungan nitrogen/karbon atau dampaknya ke tanah).
    Format Nada: Semangat, ramah, dan apresiatif.

    KATEGORI 2: OBJEK TIDAK DAPAT DIKOMPOSKAN (NON-COMPOSABLE - ANORGANIK / BAHAN BERBAHAYA)
    Jika objek yang dideteksi adalah bahan non-organik atau bahan organik yang berbahaya bagi kompos rumahan (seperti: plastik, kaca, logam, daging/tulang utuh, kotoran hewan peliharaan, kertas minyak), berikan:
    1. Kata-kata pengingat atau peringatan yang sopan tetapi jelas.
    2. Penjelasan singkat mengapa bahan tersebut tidak boleh masuk ke wadah kompos (misalnya memicu bau, mengundang hama, atau tidak bisa terurai).
    3. Solusi alternatif singkat (misal: "sebaiknya didaur ulang" atau "buang ke tempat sampah anorganik").
    Format Nada: Edukatif, mengingatkan, dan solutif.

    ATURAN TAMBAHAN:
    - Jawab secara langsung, padat, dan jelas (to-the-point). Jangan bertele-tele karena teks ini akan ditampilkan di layar aplikasi.
    - Selalu gunakan bahasa Indonesia yang santai tapi sopan.
    """

    user_prompt = f"Objek terdeteksi: '{nama_objek}'. Status bisa dikompos: {bisa_dikompos}."

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.6, # Suhu diturunkan sedikit agar AI patuh pada batas 2-3 kalimat
                max_output_tokens=150 
            )
        )
        return response.text.strip()
    except Exception as e:
        return f"Gagal mendapatkan respon AI: {str(e)}"
    
def logic_compos(label_result):
    # 1. Pengecekan jika tidak ada objek yang terdeteksi oleh YOLO
    if not label_result:
        return {
            "bisa_dikompos": False,
            "status": "Tidak Terdeteksi",
            "solusi": "Pastikan objek sampah terlihat jelas di depan kamera!",
            "edukasi_ai": "Saya tidak melihat adanya objek sampah di frame kamera."
        }

    # Standardisasi semua teks label menjadi huruf kecil
    labels_lowercase = [str(label).lower() for label in label_result]
    
    # Ambil objek utama (objek pertama yang dideteksi) untuk dijadikan bahan edukasi Gemini
    objek_utama = labels_lowercase[0]

    # 2. Filter Kaku: Deteksi apakah ada kontaminan/anorganik berbahaya
    for sampah in labels_lowercase:
        if sampah in ['plastik', 'kertas', 'kaleng', 'styrofoam', 'non organic']:
            # Panggil Gemini untuk memberikan kalimat teguran kreatif
            ai_response = generate_gemini_response(sampah, bisa_dikompos=False)
            
            return {
                "bisa_dikompos" : False,
                "status" : "Gagal / Anorganik",
                "solusi": f"Segera pisahkan '{sampah}' dari wadah kompos!",
                "edukasi_ai": ai_response
            }
        
    # 3. Jika lolos filter anorganik, berarti sampah tersebut aman/organik
    # Panggil Gemini untuk memberikan edukasi kandungan biologis/manfaat komposnya
    ai_response = generate_gemini_response(objek_utama, bisa_dikompos=True)

    return {
        "bisa_dikompos" : True,
        "status": "Organik / Aman",
        "solusi": f"Aman! Masukkan '{objek_utama}' ke dalam komposter.",
        "edukasi_ai": ai_response
    }