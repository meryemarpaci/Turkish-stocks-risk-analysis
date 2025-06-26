# Z-Skor Dönüşümü, Çarpıklık ve Basıklık Analizi Sunum Notları

## Slayt 1: Giriş
- Projenin amacı: Türk hisse senedi piyasasındaki iki hissenin (Türk Hava Yolları ve Ereğli Demir Çelik) 2020'den günümüze kadar olan fiyat hareketlerini analiz etmek
- Kullandığımız yöntemler: Z-skor dönüşümü, çarpıklık (skewness) ve basıklık (kurtosis) analizi

## Slayt 2: Teorik Altyapı

### Z-Skor Nedir?
- Z-skor (standart skor), bir veri noktasının ortalamadan standart sapma cinsinden ne kadar uzakta olduğunu gösteren bir ölçüdür
- Formül: Z = (X - μ) / σ (X: veri noktası, μ: ortalama, σ: standart sapma)
- Z-skor'un finans alanında kullanımı:
  - Anormal fiyat hareketlerinin tespiti
  - Farklı varlıkların risklerinin karşılaştırılması
  - Uç değerlerin (outlier) belirlenmesi

### Çarpıklık (Skewness) Nedir?
- Bir olasılık dağılımının asimetrisinin ölçüsüdür
- Pozitif çarpıklık: Sağ kuyruk daha uzun (nadiren büyük kazançlar)
- Negatif çarpıklık: Sol kuyruk daha uzun (nadiren büyük kayıplar)
- Normal dağılımın çarpıklık değeri 0'dır

### Basıklık (Kurtosis) Nedir?
- Bir olasılık dağılımının kuyruklarının "kalınlığının" ölçüsüdür
- Yüksek basıklık: Dağılımın kuyrukları daha kalın (aşırı değerler daha olası)
- Normal dağılımın basıklık değeri 3'tür (veya excess kurtosis için 0)
- Finansal getiriler genellikle yüksek basıklık gösterir (leptokurtik dağılım)

## Slayt 3: Veri ve Metodoloji
- Veri kaynağı: Yahoo Finance
- Zaman aralığı: 1 Ocak 2020 - Günümüz
- Analiz edilen hisseler: THYAO (Türk Hava Yolları) ve EREGL (Ereğli Demir Çelik)
- Metodoloji:
  1. Günlük kapanış fiyatlarından logaritmik getiriler hesaplandı
  2. Getiriler üzerinde Z-skor dönüşümü uygulandı
  3. Çarpıklık ve basıklık değerleri hesaplandı
  4. Aşırı hareketli günler (|Z-skor| > 2) belirlendi

## Slayt 4: THYAO Analiz Sonuçları
- Temel istatistikler (ortalama getiri, standart sapma, vb.)
- Çarpıklık ve basıklık değerleri
- Z-skor dağılımı ve zaman serisi
- Aşırı hareketli günler ve bu günlerde yaşanan önemli olaylar

## Slayt 5: EREGL Analiz Sonuçları
- Temel istatistikler (ortalama getiri, standart sapma, vb.)
- Çarpıklık ve basıklık değerleri
- Z-skor dağılımı ve zaman serisi
- Aşırı hareketli günler ve bu günlerde yaşanan önemli olaylar

## Slayt 6: Hisselerin Karşılaştırması
- Çarpıklık ve basıklık değerlerinin karşılaştırılması
- Risk ve getiri özelliklerinin karşılaştırılması
- Z-skor dağılımlarının karşılaştırılması
- Hangi hisse daha fazla aşırı hareket gösteriyor?

## Slayt 7: Pratik Uygulamalar
- Z-skor analizi, çarpıklık ve basıklık bilgisinin yatırım kararlarında nasıl kullanılabileceği
- Aşırı hareketlerden sonra fiyat davranışı üzerine gözlemler
- Risk yönetimi açısından çıkarımlar
- Portföy çeşitlendirmesi için öneriler

## Slayt 8: Sonuç ve Öneriler
- Analiz sonuçlarının özeti
- Bulunan önemli bulguların vurgulanması
- İleriki çalışmalar için öneriler
- Teşekkür ve kaynakça

## Not: Sunumda Dikkat Edilecek Noktalar
1. Teknik terimleri sadeleştirip anlaşılır şekilde açıkla
2. Görselleştirmeleri etkin kullan
3. Teorik bilgiyi gerçek dünya uygulamaları ile ilişkilendir
4. Her iki hissenin sonuçlarını yorumlarken piyasa koşullarını ve önemli olayları göz önünde bulundur 