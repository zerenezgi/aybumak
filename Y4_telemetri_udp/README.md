# Y4 — Telemetri Paketi ve UDP Haberleşmesi

## Görev nedir?
Araçtan yer istasyonuna veri gönderen bir sistem yaptım. Veriler ikili
(binary) bir pakete çevriliyor, UDP ile gönderiliyor ve yer istasyonunda
çözülüp ekrana yazılıyor. Gönderici paketlerin %5'ini bilerek bozuyor,
%2'sini hiç göndermiyor. Alıcı bozuk ve kayıp paketleri sayıyor.

## Dosyalar
- `paket.py`: `encode()` ve `decode()` fonksiyonları, checksum hesabı.
- `arac.py`: sahte verilerle saniyede 10 paket üretip UDP ile gönderir.
- `yer.py`: paketleri alır, çözer, bozuk ve kayıp paketleri sayar.

## Paket formatı
| Sıra | Alan | Tür | Bayt |
|---|---|---|---|
| 1 | Başlık (0xAA 0x55) | sabit | 2 |
| 2 | Paket numarası | uint32 | 4 |
| 3 | Zaman (ms) | uint32 | 4 |
| 4 | Enlem | double | 8 |
| 5 | Boylam | double | 8 |
| 6 | İrtifa (m) | float | 4 |
| 7 | Hız (m/s) | float | 4 |
| 8 | Batarya (V) | float | 4 |
| 9 | Sapma x | int16 | 2 |
| 10 | Sapma y | int16 | 2 |
| 11 | Kilit durumu (0/1) | uint8 | 1 |
| 12 | Checksum (XOR) | uint8 | 1 |
| | **Toplam** | | **44** |

Başlık, alıcının "bu bir paketin başı" demesini sağlıyor. Checksum, başlıktan
kilit durumuna kadar bütün baytların XOR'u. Alıcı aynı hesabı yapıp sonucu
paketin son baytıyla karşılaştırıyor. Uyuşmuyorsa paketin yolda bozulduğunu
anlıyor.

## Nasıl çalıştırılır?
Python 3.15.2 kullandım. İki ayrı terminalde, önce yer istasyonu, sonra araç:

```
cd Y4_telemetri_udp
python yer.py
python arac.py
```

`yer.py` ilk paket gelene kadar bekliyor. Paketler 3 saniye kesilince
dinlemeyi bırakıp özeti yazıyor. `arac.py` 300 paket gönderiyor ve saniyede
10 paket olduğu için 30 saniyede bitiyor. Yer istasyonunu başlatmadan aracı
çalıştırırsam paketler kayboluyor, çünkü UDP'de gönderen alıcının orada olup
olmadığına bakmıyor.

## Çıktı örneği
`yer.py` çıktısından (kısaltılmış):

```
# 1 | konum: 39.88604, 32.78106 | batarya: 12.6 V | sapma: (47, 10) | kilit: False
# 2 | konum: 39.88609, 32.78113 | batarya: 12.6 V | sapma: (-47, 11) | kilit: True
# 3 | konum: 39.88613, 32.78119 | batarya: 12.59 V | sapma: (-100, 28) | kilit: False
BOZUK PAKET: Checksum uyuşmuyor, paket bozuk.
# 5 | konum: 39.88622, 32.78132 | batarya: 12.59 V | sapma: (80, -82) | kilit: False
...
# 110 | konum: 39.89077, 32.78797 | batarya: 12.38 V | sapma: (47, 34) | kilit: True
# 112 | konum: 39.89085, 32.78809 | batarya: 12.38 V | sapma: (-53, -55) | kilit: False
...
# 299 | konum: 39.88008, 32.79497 | batarya: 12.0 V | sapma: (-2, 76) | kilit: True
3 saniyedir paket gelmiyor, bitiriyorum.
--- Yer istasyonu özeti ---
Geçerli paket: 286
Bozuk paket: 10
Kayıp paket (tahmini): 3
Ortalama paket boyutu: ikili 44 bayt, CSV 65.4 bayt
```

`arac.py` çıktısı:

```
--- Araç özeti ---
Numara verilen paket: 300
Gönderilen: 296  (bunların 10 tanesi bilerek bozuldu)
Hiç gönderilmeyen: 4
```

## Sonuçlar
| | Araç | Yer istasyonu |
|---|---|---|
| Gönderilen / alınan (geçerli + bozuk) | 296 | 286 + 10 = 296 |
| Bilerek bozulan / bozuk gelen | 10 | 10 |
| Hiç gönderilmeyen / kayıp tahmini | 4 | 3 |

- Gönderilen 296 paketin hepsi ulaştı. Araç ve alıcı aynı bilgisayarda
  olduğu için ağda gerçek bir kayıp olmadı, kayıpları ve bozulmaları ben
  simüle ettim.
- Bozuk paket sayısı birebir tuttu (10 ve 10). Alıcı bozulan paketleri
  checksum ile yakaladı.
- Kayıp sayısı 4 olması gerekirken 3 çıktı. Çıktıda #111, #163 ve #198
  numaralı paketler hiç gelmedi, bunları alıcı numara boşluğundan tespit
  etti. Dördüncü kayıp son paket (#300). Alıcı kaybı "gelen en büyük paket
  numarasına göre" hesapladığı için en son paketin kaybolduğunu fark edemedi.

## Paket boyutu: ikili ve CSV
İkili paket sabit 44 bayt. Aynı veriyi CSV satırı olarak yazsaydım
ortalama 65,4 bayt olacaktı, yani ikili paket yaklaşık üçte bir daha küçük.
CSV'de sayı uzadıkça satır uzuyor, ikili pakette boyut hep sabit olduğu
için alıcı hangi baytta ne olduğunu önceden biliyor.

## UDP ve TCP
TCP, paket ulaştı mı diye onay istiyor ve ulaşmayanı yeniden gönderiyor, bu
yüzden daha yavaş ama veri kaybının istenmediği yerlerde kullanılıyor. UDP
ise paketi gönderip ulaştı mı diye bakmıyor, bu yüzden hızlı ama bazı
paketler kaybolabilir. Telemetride araç sürekli yeni konum gönderdiği için
kaybolan eski bir paketi yeniden göndermenin anlamı yok, önemli olan en
yeni bilginin hızlı gelmesi.

## Sınırlamalar
- Veriler sahte: konum Y1'deki A → B → C rotasında ilerliyor, diğer
  değerler rastgele.
- Araç ve yer istasyonu aynı bilgisayarda (127.0.0.1) çalıştı.
- Kayıp sayısı bir tahmin, son paketler kaybolursa alıcı bunu göremiyor.
  Bu çalıştırmada olan da buydu (3 tahmin, 4 gerçek).
- XOR checksum basit bir kontrol. Bazı bozulmaları yakalayamayabilir
  (örneğin iki bayt aynı şekilde değişirse), daha güçlüsü CRC.

## Öğrendiklerim
- Struct modülü Python'daki normal verileri (sayı, yazı vb.) bilgisayarın, disklerin veya internet ağlarının doğrudan okuyabileceği ham (saf/binary) byte verisine dönüştüren bir araçtır.
- Verileri düz yazı olarak göndermek çok hantal kalıyor. Hız kazanmak için verileri sabit boyutlu kutucuklara ayırıyoruz (ilk 2 bayt şu, sonraki 4 bayt bu gibi). 
- Sistemin paketin başlangıcını anlaması için en başa bir kod koyuyoruz. Paketin sonuna da XOR (Checksum) ekliyoruz. Bu aslında TC kimlik numarasının son hanesiyle aynı mantıkta çalışıyor. Sistem veriyi doğruluyor, sonuç tutmazsa paketin yolda bozulduğunu anlayıp atıyor.
- UDP "gönder ve unut" mantığıyla çalışıyor, yani karşı taraf dinlemiyorsa paket kayboluyor. Ama uçan bir araçta 3 saniye önceki eski veriyi beklemektense anlık güncel veriyi almak daha önemli. O yüzden hız için paket kaybını göze alıp UDP kullanıyoruz.
- Paketlerin kaybolduğunu da içlerine koyduğumuz sıra numaralarından anlıyoruz (15'ten sonra 17 gelirse 16 yolda kaybolmuştur).

## Takıldığım yerler ve çözümler
- Terminalde `yer.py` ben ikinci terminali açana kadar 3 saniye sonra
  kapanıyordu. Zaman aşımını ilk paket gelene kadar sonsuz yapıp, ilk
  paketten sonra 3 saniye yaptım.
- Önce `arac.py`'yi çalıştırınca paketler kayboldu. UDP'de gönderenin
  alıcıya bakmadığını böylece gördüm.
- Terminalde `__pycache__` içinde bir `.pyc` dosyası gördüm. Python'un
  kendi oluşturduğu derlenmiş bir kopya, silmeme ya da commit etmeme gerek
  yok.

## Kaynaklar
- What is the struct Module in Python - https://youtu.be/qFOaV6uMhFQ?si=v8dPPt1A3uXpLfOp
- https://docs.python.org/3/library/struct.html
- https://en.wikipedia.org/wiki/Checksum
- https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/
- https://www-pynetlabs-com.translate.goog/udp-vs-tcp/?_x_tr_sl=en&_x_tr_tl=tr&_x_tr_hl=tr&_x_tr_pto=sge
- https://www-avast-com.translate.goog/c-tcp-vs-udp-difference?_x_tr_sl=en&_x_tr_tl=tr&_x_tr_hl=tr&_x_tr_pto=sge
- (CRC) Cyclic Redundancy Check Yöntemi (Ders: Veri İletişimi) - https://youtu.be/N0kr_eqBrwE?si=-LVTS7aidetd5-Ut ⭐
- Claude (yapay zekâ asistanı): paket formatını ve UDP mantığını anlattı,
  kodun yapısını hazırladı; ben çalıştırıp denedim ve çıktıları kendim
  inceledim.