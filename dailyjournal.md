# 19 Ekim 2026
- Süre: 20 dakika
- Ne yaptım:  Githubda ilk repomu oluşturdum ve bilgisayarıma klonladım.
- Kaynaklar: 
How To Use GitHub For Beginners - https://youtu.be/a9u2yZvsqHA?si=7Sl8LUXK_iyVvpYI
How to use Git & GitHub in VS Code - beginners tutorial - https://youtu.be/1gDkpZ0AjlQ?si=8P6Rie3raVXf8NSP

# 20 Ekim 2026
- Süre: 0 dakika
- Bilgisayara erişimim olmadı.

# 21 Ekim 2026
- Süre: 4 saat
- Ne denedim: Görev Y1'e başladım. Python'da math kütüphanesini kullanarak sin ve cos fonksiyonlarının radyan cinsinden çalıştığını fark ettim. Antigravity'de Gemini yardımıyla izleyeceğim yol haritasını çıkardım.
- Nerede takıldım: Haversine formülünü araştırırken Vincenty adında başka bir formülle karşılaştım. Haversine dünyayı küre olarak kabul ederken Vincenty dünyayı elipsoid olarak kabul ediyormuş ve hassasiyeti daha yüksekmiş. Ancak hesaplaması daha karmaşıkmış. Neden Haversine kullandığımızı anlamakta zorlandım.
- Nasıl çözdüm: Gemini yardımıyla Haversine formülünün çoğu durum için yeterli hassasiyette olduğunu ve daha basit hesaplamalar sunduğunu öğrendim. Ayrıca daha önce yapılmış bir İHA Tespit ve Takip algoritmasında da Haversine kullanıldığını gördüm.
- Kaynaklar:
https://www.scribd.com/document/256875348/Haversine-Formula
https://www.movable-type.co.uk/scripts/latlong-vincenty.html
https://getmylocations.com/blog/haversine-vs-vincenty
https://www.movable-type.co.uk/scripts/latlong.html
https://ibonav.aero/learn/havacilikta-kullanilan-yonler/
https://lnkd.in/p/dtWmfcpy

# 22 Ekim 2026
- Süre: 1 saat
- Ne yaptım: Pythonda fonksiyon tanımlamayı öğrendim. Mesafe() ve Yön() fonksiyonlarını yazmaya başladım.
- Nerede takıldım: Return komutunun ne işe yaradığını tam olarak anlayamadım.
- Nasıl çözdüm: Youtube'dan yararlandım.
- Kaynaklar:
print() vs. return in Python Functions - https://www.youtube.com/watch?v=LWdsF79H1Pg
How to calculate Distance between two city or 2 points ( lat, lon) based on Haversine Formula - https://www.youtube.com/watch?v=TOTlkKMjQfw

# 23 Ekim 2026
- Süre: 2 saat
- Ne yaptım: Python'da yeni kod blokları öğrendim. Terminalde çalışan bir program yaptım ve gerçek hayattaki iki konumla (Sultanahmet-Kızılay) test ettim ve yaklaşık olarak doğru sonuçlar verdiğini gördüm. Görev Y1'i tamamladım.
- Nerede takıldım: Daha önce görmediğim (try/except/{m:.1f}) bazı kısımları anlamakta zorlandım.
- Nasıl çözdüm: Claude'dan yardım aldım ve kod bloklarını teker teker anlatmasını ve açıklamasını istedim, kafamda oturana kadar sormaya devam ettim ayrıca tekrar döndüğümde unutmamam için # ile kodu açıklayan notlar ekledim.
- Kaynaklar:
claude.ai
https://www.movable-type.co.uk/scripts/latlong.html
Calculate Distance using Haversine Formula in Python - https://www.youtube.com/watch?v=Brl73oaLU60
Haversine Python lesson solution - https://www.youtube.com/watch?v=tPt_g2-hNLU&t=1s

# 24 Ekim 2026
- Süre: 40 dakika
- Ne yaptım: Görev Y2'ye başladım. OpenCV 5.0.0'ı kurdum. Kamera ve video okuma konusunda temel denemeler yaptım ve videonun oynatma hızının waitKey süresi ile, kameranın hızının ise kameranın kendisiyle belirlendiğini öğrendim. 
- Nerede takıldım: waitKey(25) yerine waitKey(1) yazınca kamerada fark görmedim, nedenini anlayamadım. Ayrıca kameradaki görüntünün ayna gibi olmamasını merak ettim.
- Nasıl çözdüm: waitKey'i video dosyasıyla denedim ve videonun hızlandığını gördüm. Sonra Claude ile konuşurken kameranın kendi hızında kare ürettiğini, bu yüzden waitKey süresini kısaltmanın kamerayı hızlandırmadığını öğrendim. Video dosyasında ise kareleri ne kadar hızlı istersem o kadar hızlı geliyor. Kamera görüntüsünün ayna gibi değil olduğu gibi geldiğini, ayna etkisi istersem `cv2.flip` kullanabileceğimi de öğrendim. Denedim ama hedef sapmasının sağ-sol yönü karışmasın diye kapalı bıraktım.
- Kaynaklar:
https://docs.opencv.org/3.4.20/dd/d43/tutorial_py_video_display.html
claude.ai
https://docs.opencv.org/4.13.0/d2/de8/group__core__array.html#gaca7be533e3dac7feb70fc60635adf441
https://docs.opencv.org/4.13.0/d7/dfc/group__highgui.html#ga5628525ad33f52eab17feebcfba38bd7

# 25 Ekim 2026
- Süre: 30 dakika
- Ne yaptım: RGB ve HSV arasındaki farkı öğrendim. RGB'de bir renk gölgeye düşünce üç kanalın (R, G, B) değeri de değiştiği için renk filtresi bozulabiliyor. HSV'de ise renk (Hue) parlaklıktan (Value) ayrı tutulduğu için görüntü işlemede HSV tercih ediliyor. Ayrıca Claude'un yardımıyla kırmızı rengi maskelemeyi öğrendim.
- Nerede takıldım: Maskede sadece kırmızı değil kırmızıya yakın renklerin de beyaz çıkması aklıma takıldı.
- Nasıl çözdüm: Bugün çözmedim, sadece gözlemledim. Yarın kutu, merkez ve en büyük nesneyi seçme adımlarıyla bu sorunu azaltmaya bakacağım.
- Kaynaklar:
claude.ai
RGB vs HSV Renkler Nedir? - https://www.youtube.com/watch?v=7YyUyS4c_t4

# 26 Ekim 2026
- Süre: 0 dakika
- Bilgisayara erişimim olmadı. (Kendi bilgisayarım henüz gelmediği için anneminkini kullanıyorum bu yüzden o bilgisayardayken maalesef çalışamıyorum.)

# 27 Ekim 2026
- Süre: 0 saat
- Kendi bilgisayarım henüz gelmediği için çalışamadım.

# 28 Ekim 2026
- Süre: 8 saat
- Ne yaptım: Yeni bilgisayarıma Windows kurdum.
- Nerede takıldım: Microsoft hesabım kilitlendi, bilgisayara giriş yapamadım. (sabah 5'e kadar çözüm bulmaya uğraştım)
- Nasıl çözdüm: Bir YouTube videosundan öğrendiğim yöntemle terminale girip yeni bir kullanıcı hesabı açtım, sorunlu hesabı kaldırdım.
- Kaynaklar:
Fix Your account has been disabled Please see your system administrator in Windows 11 / 10 🛠️✔️ - https://www.youtube.com/watch?v=AFVtagXCj9U&lc=UgxA-ZbWN4l3_ZbwgUN4AaABAg.AcXP43IfsIEAc_zhCk9iZ4

# 29 Ekim 2026
- Süre: 30 dakika
- Ne yaptım: Git ve Python'u kurdum, GitHub deposunu getirdim, OpenCV 5.0.0'ı kurdum.
- Nerede takıldım: `pip` komutu tanınmadı.
- Nasıl çözdüm: `python -m pip install opencv-python` yazdım.
- Kaynaklar:
claude.ai

# 30 Ekim 2026
- Süre: 1,5 saat
- Ne yaptım: 27-29 Ekim günlüklerini düzelttim. Y2'de kutu, merkez, sapma ve FPS kodunu ekledim ve kamerayla denedim. `S_ALT` değerini 150 ve 180 yaparak ten rengi sorununu azaltmayı denedim. Oyuncak ejderha ile kutuyu yan yana koyup programın alanı büyük olanı seçtiğini gördüm. `waitKey` değerini kamerada ve videoda denedim.
- Nerede takıldım: Kutu ekranda görünmüyordu çünkü `imshow` satırı çizimlerden önceydi. Ten rengi maskeye giriyordu. `S_ALT`'i yükseltince kutunun soluk kırmızı kısımları da kayboldu. Videoda sapma ve FPS yazıları görünmüyordu.
- Nasıl çözdüm: `imshow` satırlarını çizimlerden sonraya taşıdım. `S_ALT`'i 120'de bıraktım çünkü hedefi kaçırmamayı tercih ettim. Videodaki yazıların nedenini o gün bulamadım.
- Kaynaklar:
claude.ai

# 31 Ekim 2026
- Süre: 4,5 saat
- Ne yaptım: Yapay zekâ video aracıyla (Gemini Omni) üç test videosu hazırladım: beyaz ışıkta hareket eden top, loş ışık, gün ışığında hareket eden küp+top. Programı bunlarla test edip sonuçları tabloya yazdım. Ekran kaydı çektim. Y2 README'sini yazdım. Yazıların okunurluğunu iyileştirdim.
- Nerede takıldım: Test ettiğim bir videoda ekrandaki FPS ve sapma değerini gösteren yazılar görünmüyordu. İlk tahminim video çözünürlüğüydü ama yanlış çıktı.  Loş ışıkta hedef bulunamadı, birbirine yaklaşan iki nesne tek nesne gibi algılandı. README'deki program adımlarındaki k# elimeleri (kare, piksel, kontür) anlamakta zorlandım.
- Nasıl çözdüm: Yazı rengi arka planla aynı olduğu için kayboluyordu, yazının arkasına siyah kutu çizen bir yöntem kullandım. Loş ışık ve yakın nesne sorunlarını çözmedim, README'de "bozulduğu yerler" altına yazdım. Kare, piksel ve kontür kavramlarını Claude'dan temelden öğrendim.
- Kaynaklar:
claude.ai
Gemini Omni: test videolarını üretti.
How to Detect Colors in OpenCV [Python] - https://www.youtube.com/watch?v=cMJwqxskyek
https://github.com/CreepyD246/Simple-Color-Detection-with-Python-OpenCV
https://docs.opencv.org/3.4.20/d4/d73/tutorial_py_contours_begin.html

# 1 Kasım 2026
- Süre:
- Ne yaptım: 
- Nerede takıldım:
- Nasıl çözdüm:
- Kaynaklar:
claude.ai
State Machine Explained: A Beginner’s Guide - https://www.youtube.com/watch?v=sosnUnI-vco
https://docs.opencv.org/4.13.0/dc/da5/tutorial_py_drawing_functions.html
QR Kod Nasıl Çalışır? | Basit ve Hızlı Anlatım - https://youtu.be/vL7NEgGfoEk?si=Y7J3P7DsxpIfPFD3
https://docs.opencv.org/3.4.20/de/dc3/classcv_1_1QRCodeDetector.html
What is the struct Module in Python - https://youtu.be/qFOaV6uMhFQ?si=v8dPPt1A3uXpLfOp
https://docs.python.org/3/library/struct.html
https://en.wikipedia.org/wiki/Checksum
https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/