import cv2
import numpy as np  # renk aralıklarını sayı dizisi olarak vermek için
import time  # FPS hesabı için

# --- Ayarlar ---
GENISLIK = 640   # işlenen görüntünün genişliği (piksel); büyük videolar bu genişliğe küçültülür
S_ALT = 120      # doygunluk alt sınırı: düşük değerlerde soluk renkler (ten rengi gibi) de maskeye girer
V_ALT = 70       # parlaklık alt sınırı: düşük değerlerde karanlık bölgeler de maskeye girer
MIN_ALAN = 500   # bundan küçük kırmızı lekeler gürültü sayılıp yok sayılır (piksel)

# --- Renkler (OpenCV BGR sırası kullanır) ---
KUTU_RENGI = (255, 0, 255)    # mor-pembe: hedefi çevreleyen kutu
MERKEZ_RENGI = (255, 0, 0)    # mavi: hedefin merkezi
YAZI_RENGI = (255, 255, 255)  # beyaz: yazı
YAZI_CIZGI_RENGI = (0, 0, 0)  # siyah: yazının dış çizgisi


def yazi_yaz(resim, metin, konum):
    """Yazıyı siyah dış çizgili beyaz renkte yazar; her arka planda okunur."""
    # Önce kalın siyah yazı (dış çizgi)
    cv2.putText(resim, metin, konum, cv2.FONT_HERSHEY_SIMPLEX, 0.7, YAZI_CIZGI_RENGI, 4)
    # Üstüne ince beyaz yazı
    cv2.putText(resim, metin, konum, cv2.FONT_HERSHEY_SIMPLEX, 0.7, YAZI_RENGI, 2)


# 0 yazılırsa kamera açılır; video için dosya yolu yazılır
kaynak = input("Kamera için 0, video için dosya yolunu yaz: ").strip().strip('"')

# "0" yazıldıysa yazıyı sayıya çevir (cv2 kamera numarasını sayı olarak bekler)
if kaynak.isdigit():
    kaynak = int(kaynak)

# Kamerayı ya da videoyu aç
cap = cv2.VideoCapture(kaynak)

# Açılamadıysa programı durdur
if not cap.isOpened():
    print("Hata: Kaynak açılamadı.")
    exit()

onceki_zaman = time.time()  # FPS hesabı için bir önceki karenin zamanı

while True:
    # Tek bir kare (resim) oku; basarili False ise video bitti demektir
    basarili, kare = cap.read()
    if not basarili:
        print("Video bitti.")
        break

    # Görüntüyü sabit genişliğe getir (hem hızlanır hem yazılar her videoda aynı boyutta kalır)
    oran = GENISLIK / kare.shape[1]
    kare = cv2.resize(kare, None, fx=oran, fy=oran)

    # Ayna görüntüsü kullanılmıyor: sapmanın sağ/sol yönü karışmasın diye

    # Kareyi BGR'den HSV'ye çevir (OpenCV renkleri RGB değil BGR sırasında tutar)
    hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)

    # Kırmızı, renk çemberinin iki ucunda olduğu için iki aralık taranır:
    # H 0-10 ve H 170-179 (OpenCV'de H, 0 ile 179 arasındadır). Aralık biçimi: [H, S, V]
    maske1 = cv2.inRange(hsv, np.array([0, S_ALT, V_ALT]), np.array([10, 255, 255]))
    maske2 = cv2.inRange(hsv, np.array([170, S_ALT, V_ALT]), np.array([179, 255, 255]))

    # İki maskeyi birleştir: aralığa uyan pikseller beyaz, diğerleri siyah olur
    maske = cv2.bitwise_or(maske1, maske2)

    # Gürültü temizliği: küçük beyaz noktaları sil (erode), sonra nesneyi eski boyutuna getir (dilate)
    maske = cv2.erode(maske, None, iterations=2)
    maske = cv2.dilate(maske, None, iterations=2)

    # Maskedeki beyaz bölgelerin dış çizgilerini (kontür) bul
    konturlar, _ = cv2.findContours(maske, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    # Görüntünün merkezi (sapma bu noktaya göre hesaplanır)
    kare_yukseklik, kare_genislik = kare.shape[:2]
    goruntu_merkez_x = kare_genislik // 2
    goruntu_merkez_y = kare_yukseklik // 2
    cv2.circle(kare, (goruntu_merkez_x, goruntu_merkez_y), 4, YAZI_RENGI, -1)  # beyaz nokta: görüntü merkezi

    # Hedef bulunamazsa ekranda bu yazı görünür
    sapma_metni = "Hedef yok"

    if konturlar:
        # Birden fazla kırmızı nesne varsa alanı en büyük olanı seç
        en_buyuk = max(konturlar, key=cv2.contourArea)

        # MIN_ALAN'dan küçükse gürültüdür, yok sayılır
        if cv2.contourArea(en_buyuk) > MIN_ALAN:
            # Nesneyi çevreleyen dikdörtgen: sol üst köşe + genişlik/yükseklik
            x, y, genislik, yukseklik = cv2.boundingRect(en_buyuk)

            # Dikdörtgenin orta noktası = nesnenin merkezi
            merkez_x = x + genislik // 2
            merkez_y = y + yukseklik // 2

            # Hedef kutusunu ve merkez noktasını çiz
            cv2.rectangle(kare, (x, y), (x + genislik, y + yukseklik), KUTU_RENGI, 2)
            cv2.circle(kare, (merkez_x, merkez_y), 5, MERKEZ_RENGI, -1)

            # Sapma: hedef merkezi - görüntü merkezi (piksel)
            # x pozitifse hedef sağda, y pozitifse hedef aşağıda
            sapma_x = merkez_x - goruntu_merkez_x
            sapma_y = merkez_y - goruntu_merkez_y
            sapma_metni = f"Sapma: x={sapma_x} y={sapma_y}"

    # Sapma yazısı (OpenCV yazı tipi Türkçe karakter desteklemez, o yüzden ASCII)
    yazi_yaz(kare, sapma_metni, (10, 30))

    # FPS: iki kare arasındaki süreden hesaplanır
    simdi = time.time()
    fps = 1 / max(simdi - onceki_zaman, 1e-6)  # sıfıra bölmeyi engelle
    onceki_zaman = simdi
    yazi_yaz(kare, f"FPS: {fps:.1f}", (10, 60))

    # Çizimler bittikten sonra ekranda göster
    cv2.imshow("Maske", maske)
    cv2.imshow("Goruntu", kare)

    # 25 milisaniye bekle; q'ya basılırsa döngüden çık
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

# Kamerayı serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()