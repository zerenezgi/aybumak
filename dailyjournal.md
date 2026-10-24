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
- Nerede takıldım: waitKey(25) yerine waitKey(1) yazınca kamerada fark görmedim. Nedenini anlayamadım. Ayrıca kameradaki görüntü ayna gibi değildi bunu merak ettim.
- Nasıl çözdüm: waitKey komutunu video dosyasıyla denedim ve hızlandığını gördüm. Daha sonra claude ile konuşurken kameranın maksimum hızının donanım tarafından belirlendiğini, ayna görüntüsü için ise flip komutunu kullanmam gerektiğini öğrendim.
- Kaynaklar:
https://docs.opencv.org/3.4.20/dd/d43/tutorial_py_video_display.html
claude.ai
https://docs.opencv.org/4.13.0/d2/de8/group__core__array.html#gaca7be533e3dac7feb70fc60635adf441
https://docs.opencv.org/4.13.0/d7/dfc/group__highgui.html#ga5628525ad33f52eab17feebcfba38bd7