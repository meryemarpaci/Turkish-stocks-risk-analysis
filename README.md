# Türk Hisse Senedi Risk Analizi

Bu proje, Türk hisse senetlerinin risk ve dağılım özelliklerini Z-skor dönüşümü, çarpıklık (skewness) ve basıklık (kurtosis) analizi kullanarak incelemektedir. Özellikle Türk Hava Yolları (THYAO) ve Ereğli Demir Çelik (EREGL) hisseleri 2020'den günümüze kadar analiz edilmiştir.

<p align="center">
  <img src="plots/comparison.png" alt="Çarpıklık ve Basıklık Karşılaştırması" width="800">
</p>

## 📊 Proje Özeti

Bu proje şu ana analizleri gerçekleştirmektedir:

1. **Z-Skor Dönüşümü**: Günlük hisse getirilerinin standardizasyonu, anormal hareketlerin tespiti
2. **Çarpıklık (Skewness) Analizi**: Getiri dağılımlarının asimetrilerinin incelenmesi
3. **Basıklık (Kurtosis) Analizi**: Getiri dağılımlarının uç değer davranışlarının değerlendirilmesi
4. **Aşırı Hareket Günlerinin Tespiti**: Z-skoru ±2'den büyük olan günlerin belirlenmesi ve analizi

## 🔍 Temel Bulgular

### THYAO (Türk Hava Yolları):

- **Ortalama Getiri**: 0.0021
- **Standart Sapma**: 0.0273
- **Çarpıklık**: 0.2425 (Hafif sağa çarpık - nadiren büyük pozitif getiriler)
- **Basıklık**: 4.3921 (Leptokurtik - normal dağılımdan daha kalın kuyruklu)
- **Aşırı Hareketli Günler**: 76 gün (49 pozitif, 27 negatif)

<p align="center">
  <img src="plots/THYAO_IS_distribution.png" alt="THYAO Dağılım Analizi" width="800">
</p>

### EREGL (Ereğli Demir Çelik):

- **Ortalama Getiri**: Değişken (güncel değer için analiz çıktısına bakınız)
- **Standart Sapma**: Değişken (güncel değer için analiz çıktısına bakınız)
- **Çarpıklık**: Değişken (güncel değer için analiz çıktısına bakınız)
- **Basıklık**: 3.1056 (Leptokurtik - normal dağılımdan daha kalın kuyruklu)
- **Aşırı Hareketli Günler**: 67 gün (40 pozitif, 27 negatif)

<p align="center">
  <img src="plots/EREGL_IS_distribution.png" alt="EREGL Dağılım Analizi" width="800">
</p>

## 📈 Analiz Çıktıları

Her hisse senedi için aşağıdaki analizler gerçekleştirilmektedir:

1. **Getiri Dağılımı**: Histogram ve normal dağılım karşılaştırması
2. **Normal Q-Q Plot**: Getiri dağılımının normallikten sapmasının değerlendirilmesi
3. **Z-Skor Zaman Serisi**: Anormal hareketlerin zaman içinde görselleştirilmesi
4. **Kutu Grafiği**: Getiri dağılımının özeti ve aykırı değerlerin tespiti
5. **Çarpıklık ve Basıklık Karşılaştırması**: Hisselerin risk profillerinin karşılaştırılması

## 💻 Kurulum ve Kullanım

### Gereksinimler

```
pandas==2.0.0
numpy==1.24.3
matplotlib==3.7.1
yfinance==0.2.28
scipy==1.10.1
seaborn==0.12.2
```

### Kurulum

1. Bu repoyu klonlayın:
   ```
   git clone https://github.com/meryemarpaci/Turkish-stocks-risk-analysis.git
   cd Turkish-stocks-risk-analysis
   ```

2. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

### Kullanım

1. Analizi çalıştırmak için:
   ```
   python stock_analysis.py
   ```
   Veya Windows'ta:
   ```
   run_analysis.bat
   ```

2. Sonuçlar `plots` ve `data` klasörlerine kaydedilecektir.

## 🧠 Teorik Arka Plan

### Z-Skor Nedir?
Z-skor (standart skor), bir veri noktasının ortalamadan standart sapma cinsinden ne kadar uzakta olduğunu gösteren ölçüdür:

Z = (X - μ) / σ

Burada:
- X: veri noktası (günlük getiri)
- μ: ortalama
- σ: standart sapma

### Çarpıklık (Skewness) Nedir?
Bir olasılık dağılımının asimetrisinin ölçüsüdür:
- **Pozitif çarpıklık**: Sağ kuyruk daha uzun (nadiren büyük kazançlar)
- **Negatif çarpıklık**: Sol kuyruk daha uzun (nadiren büyük kayıplar)

### Basıklık (Kurtosis) Nedir?
Bir dağılımın kuyruklarının "kalınlığının" ölçüsüdür:
- **Yüksek basıklık (Leptokurtik)**: Dağılımın kuyrukları daha kalın, uç değerler daha olası
- **Düşük basıklık (Platikurtik)**: Dağılımın kuyrukları daha ince, uç değerler daha az olası

## 📑 Proje Yapısı

```
Turkish-stocks-risk-analysis/
├── stock_analysis.py       # Ana analiz kodu
├── requirements.txt        # Gerekli Python paketleri
├── run_analysis.bat        # Windows için çalıştırma dosyası
├── README.md               # Proje açıklaması (Bu dosya)
├── sunum_notlari.md        # Sunum için notlar
├── data/                   # Veri dosyaları
│   ├── THYAO_IS.csv        # THYAO hisse verileri
│   ├── EREGL_IS.csv        # EREGL hisse verileri
│   ├── THYAO_IS_extreme_days.csv # THYAO aşırı hareket günleri
│   └── EREGL_IS_extreme_days.csv # EREGL aşırı hareket günleri
└── plots/                  # Görselleştirmeler
    ├── THYAO_IS_distribution.png # THYAO dağılım analizi
    ├── EREGL_IS_distribution.png # EREGL dağılım analizi
    └── comparison.png      # Karşılaştırma grafikleri
```

## 📋 Gelecek Çalışmalar

- Daha fazla Türk hisse senedi eklemek
- Farklı zaman dilimlerinde analiz yapmak
- Makroekonomik faktörlerle korelasyon analizi
- Volatilite modelleri ile karşılaştırma (GARCH vb.)
- Anomali tespiti için makine öğrenmesi algoritmaları uygulamak

## 👩‍💻 Yazar

- **Meryem Arpacı** - [GitHub](https://github.com/meryemarpaci)

## 📜 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 