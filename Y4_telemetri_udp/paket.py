import struct

# Paket başlığı: her paketin başındaki sabit 2 bayt (alıcı paketin başladığını bundan anlar)
BASLIK = b"\xAA\x55"

# Paketin yapısı (checksum hariç). Her harf bir alanın türünü gösterir:
# <  : küçük-endian, alanlar arasında boşluk yok
# 2s : başlık (2 bayt)
# I  : paket numarası (4 bayt, işaretsiz tam sayı)
# I  : zaman, milisaniye (4 bayt, işaretsiz tam sayı)
# d  : enlem (8 bayt, ondalıklı)
# d  : boylam (8 bayt, ondalıklı)
# f  : irtifa, metre (4 bayt, ondalıklı)
# f  : hız, m/s (4 bayt, ondalıklı)
# f  : batarya gerilimi, volt (4 bayt, ondalıklı)
# h  : sapma x (2 bayt, işaretli tam sayı)
# h  : sapma y (2 bayt, işaretli tam sayı)
# B  : kilit durumu (1 bayt: 0 ya da 1)
FORMAT = "<2sIIddfffhhB"

# Toplam paket boyutu: format boyutu + 1 bayt checksum = 44 bayt
PAKET_BOYUTU = struct.calcsize(FORMAT) + 1


def xor_hesapla(veri):
    """Verideki bütün baytları XOR'layıp tek bir bayt (checksum) üretir."""
    sonuc = 0
    for bayt in veri:
        sonuc ^= bayt  # her bayt sonuca XOR'lanır
    return sonuc


def encode(paket_no, zaman_ms, enlem, boylam, irtifa, hiz, batarya, sapma_x, sapma_y, kilit):
    """Verileri 44 baytlık ikili pakete çevirir."""
    # Verileri formata göre baytlara çevir (checksum hariç)
    govde = struct.pack(FORMAT, BASLIK, paket_no, zaman_ms, enlem, boylam,
                        irtifa, hiz, batarya, sapma_x, sapma_y, int(kilit))

    # Gövdedeki bütün baytlardan checksum hesapla
    checksum = xor_hesapla(govde)

    # Checksum'ı sona ekleyip paketi döndür
    return govde + bytes([checksum])


def decode(veri):
    """İkili paketi çözüp sözlük olarak döndürür. Paket bozuksa ValueError verir."""
    # 1) Boyut kontrolü
    if len(veri) != PAKET_BOYUTU:
        raise ValueError(f"Paket boyutu yanlış: {len(veri)} bayt (beklenen {PAKET_BOYUTU})")

    # 2) Checksum kontrolü: gelen paketin checksum'ı, kendi hesapladığımızla aynı mı?
    govde = veri[:-1]
    gelen_checksum = veri[-1]
    if xor_hesapla(govde) != gelen_checksum:
        raise ValueError("Checksum uyuşmuyor, paket bozuk.")

    # 3) Baytları alanlara ayır
    (baslik, paket_no, zaman_ms, enlem, boylam,
     irtifa, hiz, batarya, sapma_x, sapma_y, kilit) = struct.unpack(FORMAT, govde)

    # 4) Başlık kontrolü
    if baslik != BASLIK:
        raise ValueError("Başlık yanlış.")

    # float alanlar 4 baytta saklandığı için küçük yuvarlama farkı oluşur; 2 basamağa yuvarlıyoruz
    return {
        "paket_no": paket_no,
        "zaman_ms": zaman_ms,
        "enlem": enlem,
        "boylam": boylam,
        "irtifa": round(irtifa, 2),
        "hiz": round(hiz, 2),
        "batarya": round(batarya, 2),
        "sapma_x": sapma_x,
        "sapma_y": sapma_y,
        "kilit": bool(kilit),
    }


# Bu dosya doğrudan çalıştırılırsa küçük bir deneme yapar
if __name__ == "__main__":
    paket = encode(1, 1500, 39.8860, 32.7810, 100.0, 15.5, 11.8, -82, -71, True)
    print("Paket (hex):", paket.hex(" "))
    print("Paket boyutu:", len(paket), "bayt")
    print("Çözülmüş:", decode(paket))

    # Aynı veriyi CSV (yazı) olarak yazsaydık kaç bayt olurdu?
    csv_satiri = "1,1500,39.8860,32.7810,100.0,15.5,11.8,-82,-71,1\n"
    print("CSV boyutu:", len(csv_satiri.encode("utf-8")), "bayt")

    # Bir baytı bilerek bozup çözmeyi dene
    bozuk = bytearray(paket)
    bozuk[10] ^= 0xFF  # 10. baytı tersine çevir (bozulma simülasyonu)
    try:
        decode(bytes(bozuk))
    except ValueError as hata:
        print("Bozuk paket yakalandı:", hata)