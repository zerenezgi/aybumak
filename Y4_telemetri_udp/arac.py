import socket
import time
import random
from paket import encode  # paket.py'daki encode fonksiyonunu kullanıyoruz

# --- Ayarlar ---
YER_ADRESI = ("127.0.0.1", 5005)  # alıcının adresi: bu bilgisayar (127.0.0.1), 5005 numaralı kapı
SANIYEDE_PAKET = 10               # saniyede kaç paket gönderilecek
TOPLAM_PAKET = 300                # toplam kaç paket gönderilecek
BOZMA_ORANI = 0.05                # paketlerin %5'i bilerek bozulacak
KAYIP_ORANI = 0.02                # paketlerin %2'si hiç gönderilmeyecek

# Y1'deki A, B, C noktaları: araç bu rotada ilerliyormuş gibi davranacak
NOKTALAR = [(39.8860, 32.7810), (39.8925, 32.7905), (39.8800, 32.7950)]


def konum_bul(adim, toplam):
    """Aracın A -> B -> C rotasında düz çizgiyle ilerlemesini taklit eder."""
    # İlerleme 0 ile 2 arasında: 0-1 arası A->B, 1-2 arası B->C
    ilerleme = adim / toplam * 2
    if ilerleme < 1:
        bas, son, oran = NOKTALAR[0], NOKTALAR[1], ilerleme
    else:
        bas, son, oran = NOKTALAR[1], NOKTALAR[2], ilerleme - 1

    # Başlangıç noktasından bitiş noktasına, orana göre ilerle
    enlem = bas[0] + (son[0] - bas[0]) * oran
    boylam = bas[1] + (son[1] - bas[1]) * oran
    return enlem, boylam


# UDP soketi: SOCK_DGRAM "paketi at ve bırak" yöntemidir (UDP)
soket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

baslangic = time.time()
gonderilen = 0   # gerçekten gönderilen paket sayısı
bozulan = 0      # bilerek bozulup gönderilenler
atlanan = 0      # hiç gönderilmeyenler

for paket_no in range(1, TOPLAM_PAKET + 1):
    # Sahte veriler (gerçek araç olmadığı için)
    zaman_ms = int((time.time() - baslangic) * 1000)
    enlem, boylam = konum_bul(paket_no, TOPLAM_PAKET)
    irtifa = 100.0 + random.uniform(-1, 1)
    hiz = 15.0 + random.uniform(-0.5, 0.5)
    batarya = 12.6 - 0.002 * paket_no          # pil yavaş yavaş azalır
    sapma_x = random.randint(-100, 100)
    sapma_y = random.randint(-100, 100)
    kilit = random.random() < 0.3              # %30 ihtimalle kilitli

    # Veriyi 44 baytlık pakete çevir
    paket = encode(paket_no, zaman_ms, enlem, boylam, irtifa, hiz, batarya,
                   sapma_x, sapma_y, kilit)

    if random.random() < KAYIP_ORANI:
        # Bu paketi hiç gönderme (kayıp simülasyonu)
        atlanan += 1
    else:
        if random.random() < BOZMA_ORANI:
            # Rastgele bir baytı bozup gönder (bozulma simülasyonu)
            bozuk = bytearray(paket)
            yer = random.randrange(len(bozuk))
            bozuk[yer] ^= 0xFF
            paket = bytes(bozuk)
            bozulan += 1

        # Paketi gönder (ulaştı mı diye sormuyoruz, UDP böyle çalışır)
        soket.sendto(paket, YER_ADRESI)
        gonderilen += 1

    # Saniyede 10 paket için 0,1 saniye bekle
    time.sleep(1 / SANIYEDE_PAKET)

print("--- Araç özeti ---")
print(f"Numara verilen paket: {TOPLAM_PAKET}")
print(f"Gönderilen: {gonderilen}  (bunların {bozulan} tanesi bilerek bozuldu)")
print(f"Hiç gönderilmeyen: {atlanan}")