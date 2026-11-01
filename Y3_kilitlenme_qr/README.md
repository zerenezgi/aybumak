# Y3 — Kilitlenme Mantığı ve QR Okuma

## Görev nedir?
Y2'deki kırmızı hedef tespitine bir kilitlenme mantığı ekledim. Ekranın
ortasında bir "vuruş alanı" dikdörtgeni var. Hedef bu alanın içinde
kesintisiz 4 saniye kalırsa ekranda KILITLENDI yazıyor ve kilitlenmenin
başlangıç ve bitiş zamanı bir dosyaya kaydediliyor. Hedef 0,2 saniyeden
kısa süre kaybolursa sayaç sıfırlanmıyor, daha uzun kaybolursa
sıfırlanıyor. Ayrıca kameraya gösterilen bir QR kodu okuyup içeriğini
ekrana yazan bir mod var.

## Dosyalar
- `y3_kilitlenme.py`: tüm kod burada.
- `kilitlenme_kayitlari.txt`: programın ürettiği kilitlenme kayıtları.
- Ekran videosu: https://drive.google.com/file/d/1p0qj1mLCiWWXCDZrqjB2TJPUAWBLnll_/view?usp=sharing

## Nasıl çalıştırılır?
Python 3.15.2 ve OpenCV 5.0.0 kullandım.

```
cd Y3_kilitlenme_qr
python y3_kilitlenme.py
```

Kaynak olarak kamera için `0`, video için dosya yolu yazılır.
- `M` tuşu: hedef modu ile QR modu arasında geçiş yapar.
- `Q` tuşu: programdan çıkar.

## Vuruş alanı
"Görüntünün %25'i büyüklüğünde" ifadesini **alanın %25'i** olarak
yorumladım. Alan, genişlik ile yüksekliğin çarpımı olduğu için her
kenarı görüntünün yarısı kadar yaptım. 640×360'lık
bir görüntüde vuruş alanı 320×180 piksel oluyor ve görüntünün tam
ortasında duruyor. Hedefin merkezi bu dikdörtgenin içindeyse hedefi
"içeride" sayıyorum.

## Kilitlenme mantığı
Programda iki zaman tutuyorum:
- `icerde_baslangic`: hedefin alana girdiği an. Alanda değilse `None`.
- `son_icerde_zamani`: hedefin alanda en son görüldüğü an.

Her karede:
1. Hedef içerideyse `son_icerde_zamani` güncellenir. Sayaç başlamadıysa
   şimdi başlatılır.
2. Hedef içeride değilse, en son içeride görüldüğünden bu yana 0,2
   saniyeden fazla geçtiyse sayaç sıfırlanır (`None` olur). 0,2
   saniyeden kısaysa sayaç devam eder. Bu toleransın sebebi, tek bir
   karede hedef kaybolsa bile sayacın bozulmaması.
3. Sayaç 4 saniyeye ulaşınca KILITLENDI yazılır.

Kilit durumu değiştiği anlarda zamanlar kaydedilir: kilit başladığında
başlangıç zamanı saklanır, kilit düştüğünde (ya da program kilitliyken
kapandığında) başlangıç ve bitiş zamanı dosyaya yazılır.

Kayıt dosyası örneği (programın gerçek çıktısı):

```
KİLİTLENDİ | Başlangıç: 16:56:22 | Bitiş: 16:56:28
```

## QR modu
`M` tuşuna basınca program hedef tespitini bırakıp kare üzerinde QR kod
arıyor (OpenCV'nin `QRCodeDetector` aracıyla). QR bulunursa çevresine
çerçeve çiziyor, içindeki yazıyı ekrana ve terminale yazıyor.

## Sınırlamalar
- Sayaç gerçek saati ölçüyor. Video dosyası kendi hızından farklı
  oynarsa "4 saniye" videonun saniyesiyle birebir uyuşmayabilir.
- Alanda birden fazla kırmızı nesne varsa sadece en büyüğü
  değerlendiriliyor.
- Loş ışıkta ve kırmızıya yakın tonlarda Y2'deki sorunlar burada da
  geçerli.
- Ekranda Türkçe harfler çizilemediği için KILITLENDI diye yazıyor,
  dosya kaydında ise Türkçe karakterli yazılıyor.

## Öğrendiklerim
- Bir durumu zamanla izlemek için değişkenleri (`icerde_baslangic`
  gibi) karelerin arasında saklamak gerekiyor. `None`, "henüz bir şey
  yok" anlamında kullanılıyor.
- Dosyaya ekleme yapmak için `open(..., "a")` kullanılıyor.
- QR kodun yönü fark etmiyor. Köşelerindeki üç büyük pozisyon işaretçisi
 sayesinde kodun yönünü ve konumunu anlar, aradaki veri modüllerini
 tarayarak bilgiyi saniyeden kısa sürede çözer. Üzeri kısmen kirlense
 veya yırtılsa bile içindeki hata düzeltme algoritmaları sayesinde
 eksik kısımları yedek verilerden tamamlayarak okumaya devam eder.

## Takıldığım yerler ve çözümler
- Kayıt dosyası kodunu koda eklerken `None` içeren birkaç değişken
  olduğu için hangisinin nereye yazılacağını karıştırdım. Claude'dan
  kodun eklenmiş halini istedim ve karşılaştırarak çözdüm.

## Kaynaklar
- https://docs.opencv.org/3.4.20/de/dc3/classcv_1_1QRCodeDetector.html
- https://www.youtube.com/watch?v=sosnUnI-vco
- Claude (yapay zekâ asistanı): kodun yapısını ve kilitlenme mantığını
  adım adım anlattı, ben yazıp denedim.
- Capcut: Kilitlenme kayıtları ve QR'ları test ettiğim videoları oluşturmada araç olarak kullandım.
- ibisPaint: QR kodlarını oluşturmamı sağladı.