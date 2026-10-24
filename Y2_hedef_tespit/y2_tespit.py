import cv2

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
    cv2.imshow("Goruntu", kare)

    # 25 milisaniye bekle; q'ya basılırsa döngüden çık
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

# Kamerayı serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()