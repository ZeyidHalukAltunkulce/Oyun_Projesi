import pygame
import modul.ayarlar as ayarlar



class Oyuncu(pygame.sprite.Sprite): # kalıtım söz konusu olduğu içi "()" kullandık, aksi halde "()" genellikle eklenmez
    ## constructer metodumuz aracılığıyla uzay gemisinin(oyuncunun) özelliklerini tanımlıyoruz
    def __init__(self, oyuncu_mermi_grup):
        # classımızı inherite ettiğimiz sprite'taki değerlere erişmek için super() sınıfımızı çağırıyoruz
        super().__init__()
        self.image = pygame.image.load("oyun_icerikleri/resim/spaceship.png") # uzay gemimizin resmini yükledik
        self.rect = self.image.get_rect()
        self.rect.centerx = ayarlar.GENISLIK // 2 # uzay gemisi nesnesinin merkez noktasının x koordinatını ortaladık  # not: ( // ) -> kalansız bölme işlemi
        self.rect.top = ayarlar.YUKSEKLIK-70 # bu sefer nesnenin üst kısmının
        self.oyuncu_mermi_grup = oyuncu_mermi_grup
        # oyuncu değişkenleri
        self.CAN = 5
        self.HIZ = 10
        # ses efekti
        self.oyuncu_mermi_sesi = pygame.mixer.Sound("oyun_icerikleri/muzik/oyuncu_mermi.wav")
    ## bu metod aracılığıyla uzay gemisinin(oyuncunun) davranışlarını(eylemlerini) tanımlıyoruz
    def update(self): # buradaki update, sprite sınıfından kalıtım yoluyla aldığımız bir metod. ilk sınıfta kullandığımızdan tamamen farklı. anladığım kadarıyla
                      # sprite grup içerisindeki bütün nesnelerin update metodları, her yeni frame oluşturulmasından önce tetiklenerek çıktıları draw(surface) ile
                      # yeni frame'e aktarılıyor. aynı zamanda bu çıktılar(konumlar vb.) sprite grubu içerisinde bir sonraki hesaplama için saklanıyor
        tus = pygame.key.get_pressed() # geriye tüm klavye tuşlarının basılma durumunu(true/false) tanımlayan bir liste döndürür
        #uzay gemimizin sol/sağ hareketlerini tanımladık
        if tus[pygame.K_LEFT] and self.rect.left >= 0: # eğer "sol tuşu basılıysa" ve "nesnenin sol kısmı sol sınıra dayanmadıysa"
            self.rect.x -= self.HIZ
        elif tus[pygame.K_RIGHT] and self.rect.right <= ayarlar.GENISLIK: # eğer "sağ tuşu basılıysa" ve "nesnenin sağ kısmı sağ sınıra dayanmadıysa"
            self.rect.x += self.HIZ
    ## oyuncuMermi sınıfını kullanarak(çağırarak), mermi ateşleme eylemini tanımlayacağız
    def ates(self):
        if len(self.oyuncu_mermi_grup) < 2: # oyuncuya ancak 2 mermi atma hakkı hakkı tanıyoruz
            self.oyuncu_mermi_sesi.play() 
            OyuncuMermi( self.rect.centerx, self.rect.top, self.oyuncu_mermi_grup )
    # biz burada space tuşuna bastığımızda, oyuncu nesnesindeki ates() metodu tetiklenecek ve böylece "OyuncuMermi()" sınıfımız çağrılacak. bu 
    # çağrılma işlemi sonrasında o sınıfın __init__(constructer) özellikleri hesaplanacak ve oluşturulan nesne çıktısı "self.oyuncu_mermi_grup"
    # grubuna yerleştirilecek

    ## oyun sekansının bir vesile(yok olma, bölüm geçme) ile sona ermesi halinde, uzay gemimizi yeniden başlama konumuna döndürüyoruz
    def reset(self):
        self.rect.centerx = ayarlar.GENISLIK // 2

class OyuncuMermi(pygame.sprite.Sprite): # oyuncu mermi gönderme işlemlerini bu sınıfta hallediyoruz
    # oyuncu mermisinin özellikleri
    def __init__(self, x, y, oyuncu_mermi_grup):
        super().__init__()
        self.image = pygame.image.load("oyun_icerikleri/resim/oyuncu_mermi.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        #mermi değişkeni
        self.HIZ = 20 ## mermi hızı
        oyuncu_mermi_grup.add(self) # bu nesneyi sprite gruba ekle ve her dongu adımında çalıştır. (hız kadar yukarı götür)
    # oyuncu mermisinin davranışları
    def update(self):
        self.rect.y -= self.HIZ
        if self.rect.bottom < 0: ## mermileri oluşturan nesneler, bir grup içerine atanarak işleniyor. pencere tepesine çarparak işlevini tammalayan mermilerin  
            self.kill()          ## artık grupta kalarak işlenmesine gerek kalmadığı için siliyoruz. (eğer bunu gerçekleştirmezsek, mermiler - sonsuzda kaybolur.)
                                 ## burada bir hedefimiz daha var: en fazla 2 mermi kullanma hakkımız olduğu için atılan mermiler silinmezse bir daha atamayız!! 