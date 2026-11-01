from datetime import datetime  # kilitlenme zamanını saat:dakika:saniye olarak yazmak için
import os  # kayıt dosyasının yolunu bulmak için
import cv2
import numpy as np  # renk aralıklarını sayı dizisi olarak vermek için
import time  # FPS hesabı için

# --- Ayarlar ---
GENISLIK = 640   # işlenen görüntünün genişliği (piksel); büyük videolar bu genişliğe küçültülür
S_ALT = 120      # doygunluk alt sınırı: düşük değerlerde soluk renkler (ten rengi gibi) de maskeye girer
V_ALT = 70       # parlaklık alt sınırı: düşük değerlerde karanlık bölgeler de maskeye girer
MIN_ALAN = 500   # bundan küçük kırmızı lekeler gürültü sayılıp yok sayılır (piksel)
KENAR_ORANI = 0.5               # vuruş alanının her kenarı görüntünün yarısı kadar (alan = %25)
VURUS_RENGI = (0, 255, 255)     # sarı: vuruş alanı dikdörtgeni
KILIT_SURESI = 4.0      # hedef bu kadar saniye kesintisiz alanda kalırsa kilitlenir
KAYIP_TOLERANSI = 0.2   # hedef bundan kısa süre kaybolursa sayaç sıfırlanmaz (saniye)

# Kayıt dosyası: bu kodun bulunduğu klasörde oluşur (hangi klasörden çalıştırılırsa çalıştırılsın)
KAYIT_DOSYASI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kilitlenme_kayitlari.txt")

# --- Renkler (OpenCV BGR sırası kullanır) ---
KUTU_RENGI = (255, 0, 255)    # mor-pembe: hedefi çevreleyen kutu
MERKEZ_RENGI = (255, 0, 0)    # mavi: hedefin merkezi
YAZI_RENGI = (255, 255, 255)  # beyaz: yazı
YAZI_CIZGI_RENGI = (0, 0, 0)  # siyah: yazının arkasındaki kutu

def yazi_yaz(resim, metin, konum):
    """Yazının arkasına siyah bir kutu çizip üstüne beyaz yazı yazar; her arka planda okunur."""
    # Yazının kaplayacağı genişlik ve yüksekliği ölç
    (yazi_genislik, yazi_yukseklik), taban = cv2.getTextSize(
        metin, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
    x, y = konum

    # Yazının arkasına dolu siyah dikdörtgen çiz (5 piksel boşluk bırakarak)
    cv2.rectangle(resim, (x - 5, y - yazi_yukseklik - 5),
                  (x + yazi_genislik + 5, y + taban + 5), YAZI_CIZGI_RENGI, -1)

    # Üstüne beyaz yazıyı yaz
    cv2.putText(resim, metin, konum, cv2.FONT_HERSHEY_SIMPLEX, 0.7, YAZI_RENGI, 2)

def kayit_yaz(baslangic, bitis):
    """Kilitlenme başlangıç ve bitiş zamanını dosyanın sonuna ekler."""
    # "a" modu: dosyayı silmeden sonuna ekler
    with open(KAYIT_DOSYASI, "a", encoding="utf-8") as dosya:
        dosya.write(f"KİLİTLENDİ | Başlangıç: {baslangic:%H:%M:%S} | Bitiş: {bitis:%H:%M:%S}\n")

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
icerde_baslangic = None   # hedefin alana girdiği an; alanda değilse None
son_icerde_zamani = 0     # hedefin alanda en son görüldüğü an
onceki_kilitli = False    # bir önceki karede kilitli miydi?
kilit_baslangic = None    # kilitlenmenin başladığı an
qr_modu = False                       # False: hedef modu, True: QR modu
qr_okuyucu = cv2.QRCodeDetector()     # QR kodu bulup çözen OpenCV aracı
son_qr_metni = ""                     # terminale aynı yazıyı tekrar tekrar basmamak için

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
    # QR modunda hedef tespiti yapılmaz, sadece QR aranır
    if qr_modu:
        # QR kodu bul ve içindeki yazıyı çöz (metin: yazı, noktalar: köşe koordinatları)
        qr_metni, qr_noktalar, _ = qr_okuyucu.detectAndDecode(kare)

        # QR bulunduysa çevresine çerçeve çiz
        if qr_noktalar is not None:
            kose_noktalari = qr_noktalar.astype(int).reshape(-1, 2)
            cv2.polylines(kare, [kose_noktalari], True, KUTU_RENGI, 3)

        # İçerik okunabildiyse ekrana yaz, değişince terminale de yaz
        if qr_metni:
            yazi_yaz(kare, f"QR: {qr_metni}", (10, 30))
            if qr_metni != son_qr_metni:
                print("QR içeriği:", qr_metni)
                son_qr_metni = qr_metni
        else:
            yazi_yaz(kare, "QR modu: QR kodu goster", (10, 30))
        yazi_yaz(kare, "M: hedef moduna don", (10, 60))

        cv2.imshow("Goruntu", kare)
        tus = cv2.waitKey(25) & 0xFF
        if tus == ord("q"):
            break
        if tus == ord("m"):
            qr_modu = False
        continue  # döngünün geri kalanını (hedef tespiti) atla
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

    # Vuruş alanı: görüntünün ortasında, alanı görüntü alanının %25'i olan dikdörtgen
    vurus_genislik = int(kare_genislik * KENAR_ORANI)
    vurus_yukseklik = int(kare_yukseklik * KENAR_ORANI)
    vurus_x1 = goruntu_merkez_x - vurus_genislik // 2   # sol kenar
    vurus_y1 = goruntu_merkez_y - vurus_yukseklik // 2  # üst kenar
    vurus_x2 = vurus_x1 + vurus_genislik                # sağ kenar
    vurus_y2 = vurus_y1 + vurus_yukseklik               # alt kenar
    cv2.rectangle(kare, (vurus_x1, vurus_y1), (vurus_x2, vurus_y2), VURUS_RENGI, 2)

    # Hedef bu karede vuruş alanının içinde mi? Varsayılan: hayır
    hedef_icinde = False
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

            # Hedefin merkezi vuruş alanının içinde mi?
            hedef_icinde = (vurus_x1 <= merkez_x <= vurus_x2 and vurus_y1 <= merkez_y <= vurus_y2)

    # Sapma yazısı (OpenCV yazı tipi Türkçe karakter desteklemez, o yüzden ASCII)
    yazi_yaz(kare, sapma_metni, (10, 30))

    zaman_simdi = time.time()

    if hedef_icinde:
        # Hedef içeride: en son görülme zamanını güncelle
        son_icerde_zamani = zaman_simdi
        # Sayaç henüz başlamadıysa şimdi başlat
        if icerde_baslangic is None:
            icerde_baslangic = zaman_simdi
    else:
        # Hedef içeride değil: tolerans süresinden uzun mu kayıp?
        if icerde_baslangic is not None and zaman_simdi - son_icerde_zamani > KAYIP_TOLERANSI:
            icerde_baslangic = None  # tolerans aşıldı, sayaç sıfırlanır

    # Sayaçta gösterilecek süre
    if icerde_baslangic is not None:
        gecen_sure = zaman_simdi - icerde_baslangic
    else:
        gecen_sure = 0.0

    # Süre kilit süresine ulaştıysa kilitli
    kilitli = gecen_sure >= KILIT_SURESI

    # Kilit durumu değiştiyse zamanı kaydet
    if kilitli and not onceki_kilitli:
        kilit_baslangic = datetime.now()               # kilitlenme anı
    elif not kilitli and onceki_kilitli:
        kayit_yaz(kilit_baslangic, datetime.now())     # kilit düştü, bitiş zamanı kaydedilir
    onceki_kilitli = kilitli

    # Sayacı ve kilit durumunu ekrana yaz (OpenCV yazı tipi Türkçe harfleri çizemez, o yüzden KILITLENDI)
    yazi_yaz(kare, f"Sayac: {gecen_sure:.1f} / {KILIT_SURESI:.0f} sn", (10, 120))
    if kilitli:
        yazi_yaz(kare, "KILITLENDI", (10, 150))

    # FPS: iki kare arasındaki süreden hesaplanır
    simdi = time.time()
    fps = 1 / max(simdi - onceki_zaman, 1e-6)  # sıfıra bölmeyi engelle
    onceki_zaman = simdi
    yazi_yaz(kare, f"FPS: {fps:.1f}", (10, 60))

    # Hedefin vuruş alanında olup olmadığını ekrana yaz
    yazi_yaz(kare, "Alan: ICINDE" if hedef_icinde else "Alan: DISINDA", (10, 90))
    yazi_yaz(kare, "M: QR modu", (10, 180))
    # Çizimler bittikten sonra ekranda göster
    cv2.imshow("Maske", maske)
    cv2.imshow("Goruntu", kare)

    # q: çıkış, m: QR moduna geç
    tus = cv2.waitKey(25) & 0xFF
    if tus == ord("q"):
        break
    if tus == ord("m"):
        qr_modu = True

# Program kilitliyken kapandıysa bitiş zamanını da kaydet
if onceki_kilitli:
    kayit_yaz(kilit_baslangic, datetime.now())

# Kamerayı serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()