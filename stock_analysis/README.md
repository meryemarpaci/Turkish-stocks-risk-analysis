# Türk Hisse Senedi Analizi

Bu proje, Türk hisse senetlerinin 2020'den günümüze kadar olan fiyat verilerini analiz eder. Z-skor dönüşümü, çarpıklık (skewness) ve basıklık (kurtosis) analizleri yaparak hisse senetlerinin risk ve dağılım özelliklerini değerlendirir.

## Özellikler

- Hisse senedi verilerinin otomatik olarak Yahoo Finance'den indirilmesi
- Günlük getirilerin hesaplanması
- Z-skor dönüşümü
- Çarpıklık ve basıklık analizi
- Aşırı hareketli günlerin tespiti
- Çeşitli görselleştirmeler:
  - Getiri dağılımı histogramları
  - Normal Q-Q grafikleri
  - Z-skor zaman serileri
  - Kutu grafikleri
  - Hisseler arası karşılaştırma grafikleri

## Kurulum

1. Python 3.8 veya daha yeni bir sürümünün kurulu olduğundan emin olun.
2. Gerekli paketleri yükleyin:

```
pip install -r requirements.txt
```

## Kullanım

1. Programı çalıştırın:

```
python stock_analysis.py
```

2. Program otomatik olarak verileri indirecek, analizleri yapacak ve sonuçları gösterecektir.
3. Grafikler `plots` klasörüne, veri dosyaları ise `data` klasörüne kaydedilecektir.

## Analiz Edilen Hisseler

Şu anda analiz edilen hisseler:
- Türk Hava Yolları (THYAO.IS)
- Ereğli Demir Çelik (EREGL.IS)

Farklı hisseleri analiz etmek istiyorsanız, `stock_analysis.py` dosyasındaki `stocks` ve `stock_names` değişkenlerini düzenleyebilirsiniz.

## Sonuçlar

Program çalıştırıldığında şu sonuçlar elde edilir:

1. Her hisse için temel istatistikler:
   - Ortalama getiri
   - Standart sapma
   - Çarpıklık (skewness)
   - Basıklık (kurtosis)
   - Maksimum ve minimum Z-skorları
   - Z-skorun ±2'yi aştığı gün sayısı

2. Aşırı hareketli günler (Z-skoru ±2'den büyük olan günler)

3. Görsel analizler:
   - Getiri dağılımı
   - Normal dağılımla karşılaştırma
   - Z-skor zaman serisi
   - Kutu grafiği 