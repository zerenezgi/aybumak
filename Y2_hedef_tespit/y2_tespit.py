import cv2
import numpy as np  # renk aralıklarını sayı dizisi olarak vermek için
# 0 yazarsan kamera açılır; video için dosya yolunu yaz
kaynak = input("Kamera için 0, video için dosya yolunu yaz: ").strip().strip('"')

# "0" yazıldıysa yazıyı sayıya çevir (cv2 kamera numarasını sayı bekler)
if kaynak.isdigit():
    kaynak = int(kaynak)

# Kamerayı ya da videoyu aç
cap = cv2.VideoCapture(kaynak)

# Açılamadıysa programı durdur
if not cap.isOpened():
    print("Hata: Kaynak açılamadı.")
    exit()

while True:
    # Tek bir kare (resim) oku; basarili False ise video bitti demektir
    basarili, kare = cap.read()
    if not basarili:
        print("Video bitti.")
        break
    # kamerayı aynalamak istersen: kare = cv2.flip(kare, 1)
    # Kareyi ekranda göster
        # Kareyi BGR'den HSV'ye çevir (OpenCV renkleri RGB değil BGR sırasında tutar)
    hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)

    # Kırmızı, renk çemberinin iki ucunda olduğu için iki aralık tarıyoruz:
    # H 0-10 ve H 170-179 (OpenCV'de H, 0 ile 179 arasındadır)
    # Aralık biçimi: [H, S, V]
    maske1 = cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255]))
    maske2 = cv2.inRange(hsv, np.array([170, 120, 70]), np.array([179, 255, 255]))

    # İki maskeyi birleştir: aralığa uyan pikseller beyaz, diğerleri siyah olur
    maske = cv2.bitwise_or(maske1, maske2)

    # Maskeyi ayrı bir pencerede göster
    cv2.imshow("Maske", maske)
    cv2.imshow("Goruntu", kare)

    # 25 milisaniye bekle; q'ya basılırsa döngüden çık
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

# Kamerayı serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()