# 🚀 Uzay Temalı 2D Aksiyon Oyunu (Python + Pygame)

Bu proje, Python programlama dili ve Pygame kütüphanesi kullanılarak geliştirilmiş başlangıç seviyesinde bir 2 boyutlu aksiyon oyunudur. Oyuncu, yatay eksende hareket eden bir uzay gemisiyle düşman uzaylılara karşı mücadele eder.


## 🎮 Oyun Özellikleri

- Uzay temalı 3 aşamalı 2D savaş oyunu
- Oyuncuya mermi atabilen düşmanlar
- Her sınır temasında aşağı doğru yaklaşan düşmanlar
- Can sistemi ve bölüm geçişleri
- Yenilgi ve tebrik ekranları
- `Enter` tuşu ile bölüme veya oyuna yeniden başlama


## 🧱 Proje Yapısı

```bash
OYUN_PROJESI/
├── main.py                  # Uygulamanın giriş noktası
├── oyun/
│   ├── oyun.py             # Oyun sınıfı
│   ├── oyuncu.py           # Oyuncu ve mermi sınıfları
│   ├── uzayli.py           # Düşman karakter sınıfları
│   └── ayarlar.py          # Sabit ayarlar (FPS, renkler vb.)
│
├── oyun_icerikleri/
│   ├── resim/              # Görseller
│   ├── muzik/              # Sesler
│   └── diger/
│
├── requirements.txt        # Gerekli bağımlılıklar
└── README.md               # Bu dosya
```


## ⚙️ Kurulum
```bash
pip install -r requirements.txt
python main.py
```


## 📚 Kullanılan Teknolojiler

- Python 3.13.3
- Pygame 2.6.1
- Visual Studio Code


## 👨‍💻 Geliştirici
- Zeyid Haluk ALTUNKÜLÇE



