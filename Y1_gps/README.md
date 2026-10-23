# Y1 — GPS ile Mesafe ve Yön

## Görev nedir?
İki GPS koordinatı (enlem, boylam) arasındaki mesafeyi metre olarak ve yönü
derece olarak (kuzey 0°, saat yönünde) hesaplayan `mesafe()` ve `yon()`
fonksiyonlarını yazdım. Sonra A → B → C rotasının her bacağı için mesafe ve
yönü, toplam rota uzunluğuyla birlikte tablo olarak yazdırdım. Program
geçersiz girişte (örneğin enlem 90'dan büyük ya da sayı olmayan değer)
çökmüyor, anlaşılır bir hata mesajı verip yeniden soruyor.

Noktalar: A (39.8860, 32.7810), B (39.8925, 32.7905), C (39.8800, 32.7950)

## Dosyalar
- `y1_gps.py`: tüm kod bu dosyada.

## Nasıl çalıştırılır?
Terminalde bu klasöre girip şunu yazın:

```
python y1_gps.py
```

Program iki seçenek sunar:
1. İki noktanın enlem ve boylamını kendiniz girersiniz; mesafe (metre) ve
   yön (derece) hesaplanır.
2. A → B → C rota tablosu yazdırılır.

## Hata kontrolü
- Sayı olmayan bir değer girilirse hata mesajı verilir ve tekrar sorulur.
- Enlem -90 ile 90, boylam -180 ile 180 arasında olmalıdır.
- Virgülle yazılan değerler (39,886 --> 39.886) noktaya çevrilir.

## Sonuçlar
Rota tablosu (programın çıktısı):

```
--- Rota tablosu ---
Bacak     Mesafe (m)    Yön (derece)
A->B          1086.0            48.3
B->C          1442.0           164.6
Toplam rota uzunluğu: 2528.0 metre
```

Gerçek dünya testi: Sultanahmet ile Kızılay arasında denedim, programın
verdiği sonuç 349.4217 km çıktı. Kıyasladığım kaynak tr.distance.to, onun değeri 349,22 km idi.

## Öğrendiklerim
- GPS koordinatları derece cinsindendir ama Python'daki `math` fonksiyonları
  (`sin`, `cos`, `atan2`) radyan bekler. Bu yüzden `math.radians()` ile
  çevirmem gerekti. Çevirmezsem program hata vermez ama sonuç yanlış çıkar,
  bu yüzden kodu gerçek bir yer çiftiyle test etmek önemli.
- Haversine, Dünya'yı mükemmel bir küre kabul eder. Araştırırken Vincenty
  formülüyle karşılaştım: o Dünya'yı elipsoid kabul ediyor, daha hassas ama
  hesabı daha karmaşık. Bizim görevdeki mesafeler kısa olduğu için aradaki
  fark çok küçük kalıyor, Haversine yeterli.
- Yön için `atan2` kullandım. `atan2` negatif açı da verebildiği için sonucu
  `% 360` ile 0-360 aralığına getirdim (örneğin -90 derece, 270 derece olur).
- Hata kontrolünü `try/except` ve `while True` ile yaptım. Kullanıcı sayı
  yerine yazı girerse `float()` hata verir, `try/except` bu hatayı yakalar
  ve program çökmeden "tekrar dene" der. `while True` döngüsü de doğru değer
  girilene kadar soruyu tekrar sorar.

## Takıldığım yerler ve çözümler
- **Haversine mi Vincenty mi:** Haversine'i araştırırken Vincenty'yi gördüm
  ve neden Haversine kullandığımızı anlamakta zorlandım. Gemini ile konuşarak
  ve kaynakları okuyarak, Haversine'in çoğu durumda yeterince hassas olduğunu
  ve daha basit hesapladığını öğrendim. Daha önce yapılmış bir İHA tespit ve
  takip algoritmasında da Haversine kullanıldığını gördüm.
- **`return` ile `print` farkı:** `return`'ün ne işe yaradığını anlamadım. Bir
  YouTube videosundan öğrendim: `print` sonucu sadece ekrana yazar, `return`
  ise sonucu fonksiyonun dışına verir ve başka yerde kullanabilirim. Mesela
  `mesafe()` sonucunu `return` ile döndürdüğüm için rota tablosunda toplam
  mesafeyi hesaplayabildim.
- **`try/except` ve `{m:.1f}` gibi yeni gördüğüm kısımlar:** Claude'dan kodun
  bölümlerini tek tek açıklamasını istedim ve kafamda oturana kadar sormaya
  devam ettim. `{m:.1f}` yazıda virgülden sonra 1 basamak göstermeyi sağlıyor.
  Tekrar döndüğümde unutmamak için koda `#` ile açıklama notları ekledim.

## Kaynaklar
https://www.scribd.com/document/256875348/Haversine-Formula
https://www.movable-type.co.uk/scripts/latlong-vincenty.html
https://getmylocations.com/blog/haversine-vs-vincenty
https://www.movable-type.co.uk/scripts/latlong.html
https://ibonav.aero/learn/havacilikta-kullanilan-yonler/
https://lnkd.in/p/dtWmfcpy
print() vs. return in Python Functions - https://www.youtube.com/watch?v=LWdsF79H1Pg
How to calculate Distance between two city or 2 points ( lat, lon) based on Haversine Formula - https://www.youtube.com/watch?v=TOTlkKMjQfw
claude.ai
Calculate Distance using Haversine Formula in Python - https://www.youtube.com/watch?v=Brl73oaLU60
Haversine Python lesson solution - https://www.youtube.com/watch?v=tPt_g2-hNLU&t=1s
https://tr.distance.to/Kızılay,Çankaya,Ankara,TUR/Sultanahmet-Bölgesi,Sultan-Ahmet,Tavukhane-Sokak,34122,Fatih,İstanbul,TUR