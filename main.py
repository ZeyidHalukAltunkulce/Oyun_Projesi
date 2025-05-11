import pygame
from modul.oyun import Oyun
from modul.oyuncu import Oyuncu, OyuncuMermi
from modul.uzayli import Uzayli, UzayliMermi
import modul.ayarlar as ayarlar

## oyunu geliştirmek için kullanacağımız "pygame" kütüphanesindeki öğeleri başlatıyorum
pygame.init()


## Mermi sprite Groupları
oyuncu_mermi_grup = pygame.sprite.Group()
uzayli_mermi_grup = pygame.sprite.Group()

## Oyuncu Tanımlama
oyuncu_grup = pygame.sprite.Group()
oyuncu = Oyuncu(oyuncu_mermi_grup)
oyuncu_grup.add(oyuncu)
# NOT: oyuncu_mermi grubu oluşturduk. sonra oyuncu_grup grubu oluşturduk. ilk oluşturduğumuz oyuncu_mermi grubunu parametre olarak vererek Oyuncu() class'ından  
#      oyuncu isimli bir nesne oluşturduk. son olarak 2. oluşturdupumuz gruba bu nesneyi ekledik. -> " oyuncu_grup.add(oyuncu) "

## Uzaylı Tanımlama
uzayli_grup = pygame.sprite.Group()
# uzayli = Uzayli(20,30,5,uzayli_mermi_grup)
# uzayli_grup.add(uzayli)
## test için:
# for i in range(10):
#     uzayli = Uzayli(i*64+64, 100, 3, uzayli_mermi_grup)
#     uzayli_grup.add(uzayli)

## oyunun çalışacağı ana yuzeyi boyutuyla beraber tanımlıyorum
pencere = pygame.display.set_mode((ayarlar.GENISLIK, ayarlar.YUKSEKLIK)) # 720p: 1280x720
# döngüsünü ve bu döngüyü kontrol edecek olan durum degiskenini tanımlıyorum
pencere_durum = [True] # özellikle liste olarak tanımladık çünkü bir nesneden, main içerisindeki bir durum değişkeninin içeriği üzerinde değişiklik yapabilmek için 
                       # referans'ının nesneye gönderilmesi gerekiyor

## oyunun ana iskeletini oluşturacak oyuncu sınıfından bir nesne türeteceğiz
oyun = Oyun(pencere_durum, pencere, oyuncu, oyuncu_mermi_grup, uzayli_grup, uzayli_mermi_grup)
## bu fonksiyonda uzaylılar (ilgili bölüme göre) tanımlanıyor:
oyun.bolum()

# ardışık resim karelerini(FPS -> while döngüsünün hızı) oluşturarak oyunun çalışma işleyişini meydana getirecek olan while 
while pencere_durum[0]:
    # bu for yapısı tek bir while adımında gerçekleştirilecek etkinlikler için yapılması gerekenleri tanımlar 
    for etkinlik in pygame.event.get():
        if etkinlik.type == pygame.QUIT:
            pencere_durum[0] = False
        if etkinlik.type == pygame.KEYDOWN: ## eğer kullanıcı bir tuşa basarsa bu algılanır
            if etkinlik.key == pygame.K_SPACE: ## algılanan space tuşu ise "oyuncu.ates()" komutu çalışır -> Oyuncu nesnesi içerisindeki ateş metodu 
                #print("space'e basıldı")
                oyuncu.ates()

    # devamlı eylemleri, yani birden çok döngü adımını kapsayacak şekilde devam eden etkinlikleri tanımlamak için while dongusu
    # govdesini kullanıyorum

    # oyunda arkaplan henüz ayarlanmadığı için eski frame'i(döngü adımı çıktısını) siyah sayfa arkaplanı ile temizliyoruz. (aksi halde her adım, önceki frame'in 
    # üzerine yazılarak ilerlediği için gölgeleme meydana gelebilir) 
    # artık oyunun iskeletini oluşturan "oyun" class'ındaki arkaplan resimlerini tanımladığımız için "pencere.fill((0,0,0))" ile siyaha boyama işlemine gerek kalmadı 
    oyun.update()
    oyun.cizdir()

    # sonraki adımda gerçekleşen yeni eylemlerin çıktıları ile grubu güncelliyoruz. ardından bu güncel grup çıktısını pencereye aktarıyoruz.  
    oyuncu_grup.update() # sprite grup içerisindeki nesnelerin tüm update metodları tetiklenerek çıktılar tekrar gruba yazılıp güncelleniyor
    oyuncu_grup.draw(pencere) # güncellenen grup bilgileri ekrana çiziliyor
    # "oyuncu = Oyuncu(oyuncu_mermi)" şeklinde nesnemizi türetirken kullandığımız "oyuncu_mermi" grubu
    oyuncu_mermi_grup.update()
    oyuncu_mermi_grup.draw(pencere)

    # test uzaylı grup
    uzayli_grup.update()
    uzayli_grup.draw(pencere)

    uzayli_mermi_grup.update()
    uzayli_mermi_grup.draw(pencere)

    # her dongu adımda oluşacak görüntü çerçevesini, o adımda gerçekleşen etkinlik sonuçları ile yeniden güncelliyorum 
    pygame.display.update()
    # döngü hızını düzenliyorum
    ayarlar.saat.tick(ayarlar.FPS)

# aktif modül öğelerini, bellekten kaldırarak oyunu tam olarak kapatıyorum
pygame.quit()






