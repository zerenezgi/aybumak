import socket
from paket import decode, PAKET_BOYUTU  # PAKET_BOYUTU: ikili paketin bayt sayısı (44)

ADRES = ("127.0.0.1", 5005)   # dinlenecek adres: bu bilgisayar, 5005 numaralı kapı

# UDP soketi açıp bu kapıyı dinlemeye başla
soket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soket.bind(ADRES)
soket.settimeout(None)  # ilk paket gelene kadar sonsuza kadar bekle

gecerli = 0         # doğru çözülen paket sayısı
bozuk = 0           # çözülemeyen (bozuk) paket sayısı
son_paket_no = 0    # gelen en büyük paket numarası
csv_toplam_bayt = 0  # aynı paketleri düz yazı (CSV) yazsaydık toplam kaç bayt olurdu

print("Dinleniyor... (önce bu programı, sonra arac.py'yi çalıştır)")

while True:
    try:
        # Bir paket gelmesini bekle
        veri, gonderen = soket.recvfrom(1024)
    except socket.timeout:
        print("3 saniyedir paket gelmiyor, bitiriyorum.")
        break
    
    # İlk paket geldi: bundan sonra 3 saniye paket gelmezse dinlemeyi bırak
    soket.settimeout(3)

    try:
        # Paketi çözmeyi dene (boyut, kontrol sayısı, damga kontrol edilir)
        p = decode(veri)
    except ValueError as hata:
        bozuk += 1
        print("BOZUK PAKET:", hata)
        continue

    gecerli += 1
        # Aynı paketi CSV satırı olarak yazsaydık kaç bayt olurdu?
    csv_satiri = (f"{p['paket_no']},{p['zaman_ms']},{p['enlem']},{p['boylam']},"
                  f"{p['irtifa']},{p['hiz']},{p['batarya']},{p['sapma_x']},"
                  f"{p['sapma_y']},{int(p['kilit'])}\n")
    csv_toplam_bayt += len(csv_satiri.encode("utf-8"))
    son_paket_no = max(son_paket_no, p["paket_no"])
    print(f"#{p['paket_no']:3d} | konum: {p['enlem']:.5f}, {p['boylam']:.5f} | "
          f"batarya: {p['batarya']} V | sapma: ({p['sapma_x']}, {p['sapma_y']}) | "
          f"kilit: {p['kilit']}")

# Kayıp tahmini: numaralar 1'den son_paket_no'ya kadar gitmişti.
# Bunların içinde geçerli gelenleri ve bozuk gelenleri çıkarınca kalan kayıptır.
kayip = son_paket_no - gecerli - bozuk

print("--- Yer istasyonu özeti ---")
print(f"Geçerli paket: {gecerli}")
print(f"Bozuk paket: {bozuk}")
print(f"Kayıp paket (tahmini): {kayip}")
if gecerli:
    print(f"Ortalama paket boyutu: ikili {PAKET_BOYUTU} bayt, CSV {csv_toplam_bayt / gecerli:.1f} bayt")