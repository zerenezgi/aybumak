# Y2 — Renkli Hedef Tespiti

## Görev nedir?
OpenCV ile kamera ya da video görüntüsünde kırmızı bir top veya balonu
tespit eden bir program yazdım. Program hedefi HSV renk filtresiyle buluyor,
etrafına kutu çiziyor, merkezini işaretliyor ve merkezin görüntü
merkezinden kaç piksel saptığını ekrana yazıyor. Ekranda ayrıca FPS
görünüyor. Birden fazla kırmızı nesne varsa en büyüğünü seçiyor.

## Dosyalar
- `y2_tespit.py`: tüm kod burada.
- Ekran videosu: https://drive.google.com/file/d/1Ax_nyF5mHErlySxb27CxFsOUs7fqlA4X/view?usp=sharing

## Nasıl çalıştırılır?
Python 3.15.2 ve OpenCV 5.0.0 kullandım (`python -m pip install opencv-python`).

```
cd Y2_hedef_tespit
python y2_tespit.py
```

Program kaynağı soruyor: kamera için `0` yaz, video için dosya yolunu
yapıştır. Çıkmak için görüntü penceresine tıklayıp `q`'ya basılır.

## Program nasıl çalışıyor?
1. Her kareyi 640 piksel genişliğe küçültüyorum (büyük videolarda yazılar
   ve hız aynı kalsın diye).
2. Kareyi BGR'den HSV'ye çeviriyorum.
3. Kırmızı için iki aralık tarıyorum (H 0-10 ve H 170-179), çünkü kırmızı
   renk çemberinin iki ucunda duruyor. İki maskeyi birleştiriyorum.
4. `erode` ve `dilate` ile küçük gürültü noktalarını siliyorum.
5. Maskedeki beyaz bölgelerin kontürlerini buluyorum ve alanı en büyük
   olanı seçiyorum. Alan 500 pikselden küçükse gürültü sayıyorum.
6. Seçilen kontürün etrafına kutu çiziyorum, kutunun orta noktasını mavi
   nokta olarak işaretliyorum.
7. Hedef merkezi ile görüntü merkezi (beyaz nokta) arasındaki farkı
   piksel olarak yazdırıyorum. x pozitifse hedef sağda, y pozitifse
   hedef aşağıda.
8. FPS'i iki kare arasındaki süreden hesaplıyorum.

## Ayarlar
- `S_ALT = 120`: doygunluk alt sınırı. Düşürürsem soluk renkler de
  maskeye girer, yükseltirsem soluk kırmızı kısımlar kaybolur.
- `V_ALT = 70`: parlaklık alt sınırı. Karanlık bölgeleri eliyor.
- `MIN_ALAN = 500`: bundan küçük lekeler gürültü sayılıyor.

## Neden RGB değil de HSV?
RGB'de bir renk gölgeye düşünce üç kanalın (R, G, B) değeri de
değişiyor, bu yüzden renk için koyduğum eşik bozulabiliyor. HSV'de renk
(Hue) parlaklıktan (Value) ayrı tutuluyor, bu yüzden renk filtresi ışık
değişince daha kararlı kalıyor.

H (Hue, ton): Hangi renk? OpenCV’de 0–179 arası. 0 civarı kırmızı, 60 civarı yeşil, 120 civarı mavi.
S (Saturation, doygunluk): Renk ne kadar canlı? 0 = soluk/gri, 255 = canlı.
V (Value, parlaklık): Ne kadar aydınlık? 0 = siyah, 255 = en parlak.

## Test sonuçları ve bozulduğu yerler
Yapay zekâ video aracıyla (Gemini Omni) üç test videosu ürettim, ayrıca kamerayla da denedim. Videolar yapay zekâyla üretilmiş görüntüler.

| Koşul | Sonuç | Not |
|---|---|---|
| Beyaz ışık, hareket eden kırmızı top | Bulundu | Hiç sorun yaşamadım |
| Loş ışık | Bulunamadı | Ekranda "Hedef yok" yazdı |
| Gün ışığı, arkada hareket eden küpler | Bulundu | İki nesne birbirine yaklaşınca tek nesne gibi algılandı |
| Kamera: ten rengi | Yanlış algılama | El de maskeye girdi |
| Kamera: kutu ve oyuncak ejderha (kamerada test ettiğim cisimler) yan yana | Büyük olanı seçti | Alan karşılaştırması çalışıyor |

Neden bozuluyor olabilir:
- **Loş ışıkta bulamaması:** Karanlıkta parlaklık (V) düşüyor ve filtremin
  alt sınırının (`V_ALT = 70`) altında kalıyor olabilir.
- **Yakın nesnelerin birleşmesi:** İki kırmızı nesne maskede birbirine
  değince tek bir beyaz bölge oluyor ve program onu tek kontür sayıyor.
- **Ten rengi:** Ten rengi kırmızıya yakın bir tonda. `S_ALT`'i 150 ve 180
  yapınca ten rengi gitti ama kutudaki soluk kırmızı bölgeler de kayboldu.
  Hedefi kaçırmamak için 120'de bıraktım.

Devam etseydim: aynı renkli yakın nesneleri ayırmak için başka bir yöntem
(örneğin şekle bakmak) araştırırdım, ve `S_ALT`/`V_ALT` değerlerini ışığa
göre otomatik ayarlamayı denerdim.

## Öğrendiklerim
- HSV'nin RGB'den farkı ve renk filtrelemede neden tercih edildiği.
- Kontür bir beyaz bölgenin sınır çizgisi. `contourArea` ile en büyüğünü
  seçebiliyorum, `boundingRect` ile etrafındaki dikdörtgeni alabiliyorum.
- Sapma, hedefin görüntü ortasından kaç piksel uzakta olduğu. Bir aracın
  hedefe dönerken kullanacağı bilgi.
- `waitKey(25)` videoyu yavaşlatıyor. Kamerada `waitKey(1)` fark yaratmadı
  çünkü kamera kendi hızında (yaklaşık 31 FPS) kare veriyor. Videoda
  `waitKey(1)` ile video hızlandı.
- `imshow`'u çizimden önce çağırırsam çizimler ekranda görünmüyor.

## Takıldığım yerler ve çözümler
- **Kutu görünmüyordu:** `imshow` satırı kutu çizen koddan önceydi. Satırı
  en alta taşıyınca çözüldü.
- **Yazılar yeşil perde videosunda görünmüyordu:** Yazı rengi ilk denediğim videodaki
  arka planla aynıydı (yeşil). İlk tahminim video çözünürlüğüydü, yanlış çıktı.
  Yazıyı siyah dış çizgili beyaz yapınca her arka planda okunur oldu.
- **`pip` komutunu tanımadı:** `python -m pip install opencv-python`
  komutuyla çözdüm.
- **Kamera ayna gibi değildi:** `cv2.flip` ile aynalamayı denedim, ama
  sapmanın sağ/sol yönü karışmasın diye kapalı bıraktım.

## Kaynaklar
- RGB vs HSV Renkler Nedir? - https://www.youtube.com/watch?v=7YyUyS4c_t4
- Claude (yapay zekâ asistanı): kodun yapısını, HSV mantığını ve hata
  ayıklamayı adım adım anlattı. Her bölümü çalıştırıp denedim.
- Gemini Omni: test videolarını üretti.
- How to Detect Colors in OpenCV [Python] - https://www.youtube.com/watch?v=cMJwqxskyek
- https://github.com/CreepyD246/Simple-Color-Detection-with-Python-OpenCV
- https://docs.opencv.org/3.4.20/d4/d73/tutorial_py_contours_begin.html