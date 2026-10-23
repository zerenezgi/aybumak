# print(math.sin(90)) output: 0.8939966636005579
# print(math.sin(math.radians(90))) output: 1.0
# sonuc: Python'da trigonometrik fonksiyonlar radyan cinsindendir. Bu yüzden dereceden radyana çevirmek gerekir.
# bearing: bir yönün kuzeyden başlayıp saat yönünde ölçülen açısı
# kuzey: 0 derece, doğu: 90 derece, güney: 180 derece, batı: 270 derece

import math

# Dünya'nın ortalama yarıçapı (metre cinsinden)
DUNYA_YARICAPI = 6371000


def koordinat_kontrol(enlem, boylam):
    """Koordinatların sayı olup olmadığını ve geçerli aralıkta olup olmadığını kontrol eder."""   
    try: # bu kral olmasa program cokerdi
        enlem = float(enlem) # sayıya çevirmeyi dene
        boylam = float(boylam)
    except (ValueError, TypeError): # "abc" gibi bir şey gelip patlarsa buraya gel
        raise ValueError("Enlem ve boylam sayı olmalı.")

    # Enlem -90 (güney kutbu) ile 90 (kuzey kutbu) arasındadır
    if not -90 <= enlem <= 90:
        raise ValueError(f"Enlem -90 ile 90 arasında olmalı, girilen: {enlem}")

    # Boylam -180 (batı) ile 180 (doğu) arasındadır
    if not -180 <= boylam <= 180:
        raise ValueError(f"Boylam -180 ile 180 arasında olmalı, girilen: {boylam}")

    return enlem, boylam

# Haversine
# Koordinatları kontrol et
# Dereceleri radyana çevir. sin ve cos radyanla çalışıyor.
# Haversine formülünü uygula.
# cos'la çarpmanın nedeni boylamların kutuplara doğru birbirine yaklaşmasından.
# atan2 ve sqrt ile iki nokta arasındaki açıyı buluyor.
# Yay uzunluğu = yarıçap × açı. Bu açıyı Dünya'nın yarıçapıyla çarpınca metre çıkar

def mesafe(enlem1, boylam1, enlem2, boylam2):
    """İki nokta arasındaki mesafeyi metre olarak döndürür (haversine)."""
    # Önce girişleri kontrol et
    enlem1, boylam1 = koordinat_kontrol(enlem1, boylam1)
    enlem2, boylam2 = koordinat_kontrol(enlem2, boylam2)

    # Enlemleri dereceden radyana çevir (cos için lazım)
    enlem1_rad = math.radians(enlem1)
    enlem2_rad = math.radians(enlem2)

    # İki nokta arasındaki enlem ve boylam farkları (radyan cinsinden)
    fark_enlem = math.radians(enlem2 - enlem1)
    fark_boylam = math.radians(boylam2 - boylam1)

    # Haversine'in "a" adımı: enlem farkının katkısı + boylam farkının katkısı
    # (boylam kısmı cos ile çarpılıyor çünkü boylam kutuplara doğru daralır)
    yari_kiris_karesi = (math.sin(fark_enlem / 2) ** 2
                         + math.cos(enlem1_rad) * math.cos(enlem2_rad)
                         * math.sin(fark_boylam / 2) ** 2)

    # Haversine'in "c" adımı: iki nokta arasındaki açı (radyan), Dünya'nın merkezinden bakınca
    aci = 2 * math.atan2(math.sqrt(yari_kiris_karesi),
                         math.sqrt(1 - yari_kiris_karesi))

    # Yay uzunluğu = yarıçap x açı  ->  metre cinsinden mesafe
    return DUNYA_YARICAPI * aci


def yon(enlem1, boylam1, enlem2, boylam2):
    """1. noktadan 2. noktaya yönü derece olarak döndürür (kuzey = 0, saat yönünde)."""
    # Önce girişleri kontrol et
    enlem1, boylam1 = koordinat_kontrol(enlem1, boylam1)
    enlem2, boylam2 = koordinat_kontrol(enlem2, boylam2)

    # Radyana çevirmeler
    enlem1_rad = math.radians(enlem1)
    enlem2_rad = math.radians(enlem2)
    fark_boylam = math.radians(boylam2 - boylam1)

    # "Doğu" bileşeni: ne kadar doğuya gidiyoruz
    dogu_bilesen = math.sin(fark_boylam) * math.cos(enlem2_rad)

    # "Kuzey" bileşeni: ne kadar kuzeye gidiyoruz
    kuzey_bilesen = (math.cos(enlem1_rad) * math.sin(enlem2_rad)
                     - math.sin(enlem1_rad) * math.cos(enlem2_rad)
                     * math.cos(fark_boylam))

    # atan2(doğu, kuzey) açıyı verir; radyandan dereceye çeviriyoruz
    yon_derece = math.degrees(math.atan2(dogu_bilesen, kuzey_bilesen))

    # Negatif çıkan açıları 0-360 aralığına getir (-90 -> 270 gibi)
    return (yon_derece + 360) % 360


def sayi_al(soru, alt_sinir, ust_sinir):
    """Kullanıcıdan sayı ister; geçersizse hata mesajı verip tekrar sorar."""
    while True:
        # Virgülle yazılırsa (39,886) noktaya çevir
        giris = input(soru).strip().replace(",", ".") # strip bosluklari siler replace ,u .ya cevirir

        # Sayı mı diye bak
        try:
            sayi = float(giris)
        except ValueError:
            print("Hata: Lütfen sayı gir (örnek: 39.8860). Tekrar dene.")
            continue # dongunun basina don tekrar sor

        # Aralıkta mı diye bak
        if alt_sinir <= sayi <= ust_sinir:
            return sayi
        print(f"Hata: Değer {alt_sinir} ile {ust_sinir} arasında olmalı. Tekrar dene.")


def iki_nokta_hesapla():
    """Kullanıcıdan iki nokta alıp mesafe ve yönü yazdırır."""
    print("\n--- İki nokta arası mesafe ve yön ---")
    enlem1 = sayi_al("1. noktanın enlemini giriniz (-90 ile 90 arası): ", -90, 90)
    boylam1 = sayi_al("1. noktanın boylamını giriniz (-180 ile 180 arası): ", -180, 180)
    enlem2 = sayi_al("2. noktanın enlemini giriniz (-90 ile 90 arası): ", -90, 90)
    boylam2 = sayi_al("2. noktanın boylamını giriniz (-180 ile 180 arası): ", -180, 180)

    m = mesafe(enlem1, boylam1, enlem2, boylam2)
    y = yon(enlem1, boylam1, enlem2, boylam2)
    print(f"Mesafe: {m:.1f} metre") # {m:.1f} demek "virgülden sonra 1 basamak göster" demek. f float, .1 bir basamak.
    print(f"Yön: {y:.1f} derece (kuzeyden saat yönünde)")


def rota_tablosu():
    """A -> B -> C rotasının her bacağı için mesafe ve yönü tablo olarak yazdırır."""
    # Noktalar: (isim, enlem, boylam)
    noktalar = [
        ("A", 39.8860, 32.7810),
        ("B", 39.8925, 32.7905),
        ("C", 39.8800, 32.7950),
    ]

    print("\n--- Rota tablosu ---")
    print(f"{'Bacak':<8}{'Mesafe (m)':>12}{'Yön (derece)':>16}")

    toplam_mesafe = 0
    # Her seferinde bir nokta ile sonrakini al (A-B, sonra B-C)
    for i in range(len(noktalar) - 1):
        isim1, enlem1, boylam1 = noktalar[i]
        isim2, enlem2, boylam2 = noktalar[i + 1]

        m = mesafe(enlem1, boylam1, enlem2, boylam2)
        y = yon(enlem1, boylam1, enlem2, boylam2)
        toplam_mesafe += m  # toplam rota uzunluğuna ekle

        print(f"{isim1 + '->' + isim2:<8}{m:>12.1f}{y:>16.1f}")

    print(f"Toplam rota uzunluğu: {toplam_mesafe:.1f} metre")


# Program buradan başlar (dosya doğrudan çalıştırıldığında)
if __name__ == "__main__":
    print("1) İki nokta arası hesapla (kendi koordinatlarımı gireceğim)")
    print("2) A -> B -> C rota tablosunu göster")
    secim = sayi_al("Seçiminiz (1 veya 2): ", 1, 2)

    if secim == 1:
        iki_nokta_hesapla()
    else:
        rota_tablosu()