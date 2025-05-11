import pygame
import random
import modul.ayarlar as ayarlar


class Uzayli(pygame.sprite.Sprite):
    def __init__(self, x, y, HIZ, uzayli_mermi_grup):
        super().__init__() # kalıtım vesilesiyle sprite'ın içerisindeki öğelere erişmek istiyoruz
        # uzaylılar "önce sag tamamla sonra sol" hareketi döngüsünü gerçekleştirmesi ve her döngü başlangıcında bir kademe bize(aşağı) yaklaşması için:
        self.YON = 1
        self.HIZ = HIZ
        if self.HIZ == 1:
            self.image = pygame.image.load("oyun_icerikleri/resim/monster1.png")
        elif self.HIZ == 2:
            self.image = pygame.image.load("oyun_icerikleri/resim/monster2.png")
        else:
            self.image = pygame.image.load("oyun_icerikleri/resim/monster3.png")

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) # uzayli nesnesinin sol üst noktasını (x, y) koordinatına yerleştirdik 
        self.uzayli_mermi_grup = uzayli_mermi_grup
        # uzaylı mermi ses efekti
        self.uzayli_mermi_sesi = pygame.mixer.Sound("oyun_icerikleri/muzik/uzayli_mermi.wav")
        # uzaylilar tarafından vurulmamız veya bir sonraki bölüme geçmemiz halinde uzaylıları varsayılan başlangıç konumlarını geri döndürmek için konumlarını kaydedelim:
        self.bas_x = x
        self.bas_y = y
    ## uzaylıların otomatik sola-sağa gidip gelme hareketini ve rastgele ateş etme eylemlerini tanımlıyoruz  
    def update(self):
        self.rect.x += self.YON * self.HIZ # şuanlık sağa gitmeyi tanımladık. bölümleri tanımlayacağımız Oyun sınıfına geçtiğimizde diğer aşamalarıda gerçekleştireceğiz
        # "(0,100) > 99" demek “%1 ihtimalle gerçekleşecek bir olayı yakalayabilir miyim?” anlamına gelir
        # Çünkü: 0 ile 100 arası → 101 sayı vardır. Bunlardan sadece biri (100) bu koşulu True yapar Dolayısıyla Bu ifade True → yaklaşık %1 olasılıkla olur. Geri 
        # kalan durumda False döner (yaklaşık %99)
        # Bu tarz yapılar genelde:  #  -Düşman nesnesi oluşturmak (%1 ihtimalle ortaya çıkacak)
                                    #  -Şanslı durumlar / ödüller
                                    #  -Rastgele olaylar (rare spawn)
        if random.randint(0,100) > 99 and len(self.uzayli_mermi_grup) < 3: # %1 ihtimalle ve toplam mermi sayısı 3'den küçükse
            self.uzayli_mermi_sesi.play()
            self.ates()

    ## uzaylıların mermi ateşleme eylemi: 
    def ates(self):
        UzayliMermi(self.rect.centerx, self.rect.bottom, self.uzayli_mermi_grup)
    ## eğer oyuncu yenilirse veya bölüm atlarsa, varsayılan konuma geri dönülmesi gerekir
    def reset(self): 
        self.rect.topleft = (self.bas_x, self.bas_y)
        self.YON = 1

        
class UzayliMermi(pygame.sprite.Sprite):
    def __init__(self, x, y, uzayli_mermi_grup):
        super().__init__() # sprite kalıtım sınıfı içeirisindeki tüm özelliklere erişmek istiyoruz
        self.image = pygame.image.load("oyun_icerikleri/resim/uzayli_mermi.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        uzayli_mermi_grup.add(self)
        self.HIZ = 10
    def update(self):
        self.rect.y += self.HIZ
        if self.rect.top > ayarlar.YUKSEKLIK: # hem gereksiz mermi nesnesi hesaplamlarını sonlandırmak hemde mermi nesnesi grubunu boşaltarak, en fazla 3 adet olacak
            self.kill()               # şekilde yeniden rastgele düşman mermisi oluşturmak için tavana ulaşıp işini bitiren mermi nesnelerini sonlandırıyoruz.
