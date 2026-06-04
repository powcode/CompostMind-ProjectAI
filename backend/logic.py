def logic_compos(label_result):


    if not label_result:
        return{
            "bisa_dikompos": False,
            "status": "Tidak Terdeteksi",
            "solusi": "Pastikan objek sampah terlihat jelas di depan kamera!"
        }

    labels_lowercase = [str(label).lower() for label in label_result]
    for sampah in labels_lowercase:
        if sampah in ['plastik', 'kertas', 'kaleng', 'styrofoam']:
            return{
                "bisa_dikompos" : False,
                "status" : "Gagal",
                "solusi": f"Segera pisahkan '{sampah}'!"
            }
        
    return{
        "bisa_dikompos" : True,
        "status": "Organik",
        "solusi": "Aman! ini adalah materi organik!"
    }
        
    # if 'kompos_matang' in label_result:
    #     return{
    #         "bisa_dikompos": True,
    #         "status": "Matang Sempurna!",
    #         "kekurangan": "Tidak ada",
    #         "solusi": "Kompos sudah siap dipanen!"
    #     }
    
    # ada_hijau = any(x in ['sayur', 'buah', 'daun_hijau'] for x in label_result)
    # ada_cokelat = any(x in ['daun_kering', 'kardus', 'ranting'] for x in label_result)

    # if 'kompos_basah_busuk' in label_result:
    #     return{
    #         "bisa_dikompos" : True,
    #         "status" : "Kondisi Kurang Baik(Teralu Basah)",
    #         "kekurangan": "Kurang Oksigen / Teralu Banyak Air",
    #         "solusi": "Aduk tumpukan"
    #     }
    
    # if "kompos_kering" in label_result:
    #     return{
    #         "bisa_dikompos": True,
    #         "status": "Kondisi teralu kering",
    #         "kekurangan": "Kurang Air",
    #         "solusi": "Semprotkan sedikit air"
    #     }
    
    # if ada_hijau and not ada_cokelat:
    #     return{
    #         "bisa_dikompos": True,
    #         "status": "Sedang Diproses",
    #         "kekurangan": "Kurang Bahan Cokelat",
    #         "solusi": "Tambahkan daun kering"
    #     }
    # elif ada_cokelat and not ada_hijau:
    #     return{
    #         "bisa_dikompos": True,
    #         "status": "Sedang Diproses",
    #         "kekurangan": "Kurang Bahan Hijau",
    #         "solusi": "Tambahkan sisa sayuran dapur"
    #     }
    

    # return{
    #     "bisa_dikompos": True,
    #     "status": "🏃 Proses Berjalan Baik",
    #     "kekurangan": "Tidak ada, rasio sudah seimbang",
    #     "solusi": "Kondisi tumpukan sudah ideal. Cukup pantau berkala!"
    # }

