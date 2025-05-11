import pygame
import modul.ayarlar as ayarlar
import modul.uzayli


class Oyun:
    # Kontrol mekaniklerini sağlayabilmek için 4 parametre tanımlıyoruz
    def __init__(self, pencere_durum, pencere, oyuncu, oyuncu_mermi_grup, uzayli_grup, uzayli_mermi_grup):
        # Oyun Değişkenleri
        self.BOLUM_NO = 1
        self.PUAN = 0
        self.vuruldukmu = False
        # Nesneler
        self.oyuncu = oyuncu
        print(type(self.oyuncu))
        self.oyuncu_mermi_grup = oyuncu_mermi_grup
        self.uzayli_grup = uzayli_grup
        self.uzayli_mermi_grup = uzayli_mermi_grup
        self.pencere = pencere
        self.pencere_durum = pencere_durum
        # Arkaplan
        self.arka_plan_1 = pygame.image.load("oyun_icerikleri/resim/arka_plan11.jpg")
        self.arka_plan_2 = pygame.image.load("oyun_icerikleri/resim/arka_plan22.jpg")
        self.arka_plan_3 = pygame.image.load("oyun_icerikleri/resim/arka_plan33.jpg")
        self.tebrikler = pygame.image.load("oyun_icerikleri/resim/tebrikler.png")
        # Şarkı ve Ses Efekti
        self.oyuncu_vurus = pygame.mixer.Sound("oyun_icerikleri/muzik/oyuncu_vurus.wav")
        self.uzayli_vurus = pygame.mixer.Sound("oyun_icerikleri/muzik/uzayli_vurus.wav")
        pygame.mixer.music.load("oyun_icerikleri/muzik/arka_plan_sarki.wav")
        pygame.mixer.music.play(-1) # '-1' ile sonsuz döngü şeklinde şarkı oyun süresince sürekli çalmaya devam eder 
        # istenildiği takdirde harici bir kaynaktan font(yazı tipi) dahil edilebilir örn -> self.oyun_font = pygame.font.Font("oyun_font.ttf", 64)
        # ben pygame içerisindeki font listesinden birini seçtim:
        # pygame.font.get_fonts() -> yerleşik font(yazı tipi) listesi döndürür 
        self.oyun_font = pygame.font.SysFont("arial", 42)

    def update(self): # temas var mı yok mu?, bölüm tamamlandı mı? uzaylıların hareketi?
        self.uzayli_konum_degistirme()
        self.temas()
        self.tamamlandi()

    def cizdir(self): # arayüz tasarımı (arkaplan resimleri ve yazılar)
        PUAN_etiketi = self.oyun_font.render("Skor:"+str(self.PUAN), True, (255,0,255), (0,0,0))
        PUAN_etiketi_konumu = PUAN_etiketi.get_rect()
        PUAN_etiketi_konumu.topleft = (20,10)

        BOLUM_NO_etiketi = self.oyun_font.render("Bölüm:"+str(self.BOLUM_NO), True, (255,0,255), (0,0,0))
        BOLUM_NO_etiketi_konumu = BOLUM_NO_etiketi.get_rect()
        BOLUM_NO_etiketi_konumu.topleft = (ayarlar.GENISLIK-190, 10)

        # normalde frame geçişlerini siyah ekran ile boyuyarak güncelliyorduk ama artık oyundaki bölüme göre arkaplan resmini güncelliyoruz.
        if self.BOLUM_NO == 1:
            self.pencere.blit(self.arka_plan_1, (0,0))
        elif self.BOLUM_NO == 2:
            self.pencere.blit(self.arka_plan_2, (0,0))
        elif self.BOLUM_NO == 3:
            self.pencere.blit(self.arka_plan_3, (0,0))
        else:
            self.bitis() # oyun canlarımız bitip yenilmeden, kazanıldıysa

        self.pencere.blit(BOLUM_NO_etiketi, BOLUM_NO_etiketi_konumu)
        self.pencere.blit(PUAN_etiketi, PUAN_etiketi_konumu)

    def uzayli_konum_degistirme(self): # uzaylı sağa/sola gitme ve döngü devamında bir birim aşağı yaklaşma
        HAREKET, CARPISMA = False, False
        for uzayli in self.uzayli_grup.sprites():
            # eğer uzaylılardan her hangi biri sağ veya sol sınıra temas ederse 
            if uzayli.rect.left <= 0 or uzayli.rect.right >= ayarlar.GENISLIK:
                HAREKET = True
        if HAREKET == True: # her uzaylı teker teker diğer yöne döndürülür ve bir kademe daha uzay gemisine yaklaştırılır
            for uzayli in self.uzayli_grup.sprites():
                uzayli.rect.y += 20 * self.BOLUM_NO # bu yaklaşma bölüm zorluğuna(numara katsayısının yaklaştırma oranına) göre belirlenir
                uzayli.YON *= -1 # for döngüsü boyunca hayatta kalan bütün uzaylıların yönü değiştirilir
                if uzayli.rect.bottom >= ayarlar.YUKSEKLIK-90: # eğer uzaylılar tavana erişmeyi başarırsa bir can azalır ve hala can hakkı kalmışsa bütün unsurlar 
                    CARPISMA = True                    # bölüm başındaki konumlarına geri döndürülerek mücadeleye yeninden başlanır
        if CARPISMA == True:
            self.oyuncu.CAN -= 1
            self.oyun_durumu() # can varsa o bölümü yeniden dene, yoksa oyuna sil baştan başla 
                
            
    def temas(self): # ateş adildiğinde temas durumu
        ## eğer mermimiz uzaylıya temas ederse?!
        if pygame.sprite.groupcollide(self.oyuncu_mermi_grup, self.uzayli_grup, True, True): # ("mermimiz", "herhangi bir uzaylı", "temas sonrası mermi yok olsun mu?", "temas sonrası uzayli yok olsun mu?")
            self.oyuncu_vurus.play()
            self.PUAN += 100 * self.BOLUM_NO # her bölümün zorluğuna göre daha fazla puan kazanılıyor 
        if pygame.sprite.spritecollide(self.oyuncu, self.uzayli_mermi_grup, True): # "groupcollide" ile grup->grup, "spritecollide" ile tek->grup teması inceleniyor. (.., .., "temas sonrası oyuncu yok olsun mu?")
            self.uzayli_vurus.play()
            self.oyuncu.CAN -= 1
            self.vuruldukmu = True
            self.oyun_durumu()

    def bitis(self): # bölüm sonu (oyunu başarılı bir şekilde tamamladık ve arkaplan bunu bize bildirdi. eğer enter tuşuna basılırsa oyun yeniden başlayacak)
        self.pencere.blit(self.tebrikler, (0,0))
        pygame.display.update()
        bittimi = True
        while bittimi:
            for etkinlik in pygame.event.get():
                if etkinlik.type == pygame.KEYDOWN:
                    if etkinlik.key == pygame.K_RETURN:
                        self.oyun_reset() # enter'a basıldığı için tamamlanan oyunu yeniden başlatacak düzenlemeleri gerçekleştiriyoruz
                        bittimi = False
                if etkinlik.type == pygame.QUIT:
                    bittimi = False
                    self.pencere_durum[0] = False

    # oyun giderek artan zorluklara sahip 3 bölümden oluşuyor. bunları tanımlıyoruz: 
    def bolum(self):
        for i in range(13):
            for j in range(2):
                uzayli = modul.uzayli.Uzayli(i*75+100, j*75+125, self.BOLUM_NO, self.uzayli_mermi_grup)
                self.uzayli_grup.add(uzayli)

    # öyle bir ayarlama yapmamız gerekiyorki, uzayli gemiye çartığında, can azalıyorsa ama bitmiyorsa, geriye kalan uzaylı grubu bölüm başındaki
    # konumlarına geri döndürülerek mücadeleye kaldığımız yerden devam etmeliyiz
    def oyun_durumu(self):
        self.oyuncu_mermi_grup.empty() # mermileri sildik
        self.uzayli_mermi_grup.empty()
        self.oyuncu.reset() # uzay gemisini ortalayarak, bölüm başındaki varsayılan konumuna döndürdük
        # kalan uzaylıları, bölüm başında oluşturuldukları konumlara geri döndürüyoruz.
        for uzayli in self.uzayli_grup.sprites():
            uzayli.reset()
        # bu sefer farklı can durumuna göre yapılacakları tanımlıyoruz
        if self.oyuncu.CAN == 0:
            self.oyun_reset() # hiç can kalmadıysa oyun baştan(1. bölümden) başlatılır
        else:
            self.durdur() # oyun durdurulur. hala can(yeniden mücadele etme şansı) olduğu için oyuncunun soluklanırken durum hakkında bilgilendirilecği 
                          # bir arayüz gösterilir 
            
    ## eğer bölüm tamamlandıysa
    def tamamlandi(self):
        if not self.uzayli_grup:
            self.BOLUM_NO += 1
            self.bolum()

    ## uzaylılar tarafınfan vurulduğumuz zaman yaşanacakları tanımlıyoruz
    def durdur(self):
        # not: oyun yukarısında can ve bölüm bilgilerini göstermek için kullandığımız oyun_font büyüklüğü buna göre küçük. bu yüzden burada farklı bir font sisteminin tanımlanması gerekebilir
        if self.vuruldukmu:
            metin1 = self.oyun_font.render("Uzaylılar tarafından vuruldunuz", True, (0,110,0), (255,0,0))
            metin1_konum = metin1.get_rect()
            metin1_konum.topleft = (100, 150)
            self.vuruldukmu = False
        else:
            metin1 = self.oyun_font.render("Uzaylılar, size ulaşmayı başardı", True, (0,110,0), (255,0,0))
            metin1_konum = metin1.get_rect()
            metin1_konum.topleft = (100, 150)

        metin2 = self.oyun_font.render(str(self.oyuncu.CAN)+" canınız kaldı!", True, (0,110,0), (255,0,0))
        metin2_konum = metin2.get_rect()
        metin2_konum.topleft = (100, 250)

        metin3 = self.oyun_font.render("Kaldığınız yerden devam etmek için 'ENTER' tuşuna basınız!", True, (0,110,0), (255,0,0))
        metin3_konum = metin3.get_rect()
        metin3_konum.topleft = (100, 350)

        self.pencere.blit(metin1, metin1_konum)
        self.pencere.blit(metin2, metin2_konum)
        self.pencere.blit(metin3, metin3_konum)
        pygame.display.update()

        durdumu = True
        while durdumu:
            for etkinlik in pygame.event.get():
                if etkinlik.type == pygame.KEYDOWN:
                    if etkinlik.key == pygame.K_RETURN:
                        durdumu = False
                if etkinlik.type == pygame.QUIT: # burada "keydown"un aksine bütün oyun durumlarında yer alan bir butona tıklama eylemi gerçekleşiyor. bu yüzden ayrı bir şekilde tanımladık
                    durdumu = False
                    self.pencere_durum[0] = False

    # oyunu baştan başlatacak hale getiriyoruz
    def oyun_reset(self):
        #oyun değişkenlerini varsayılan olacak şekilde sıfırladık
        self.vuruldukmu = False
        self.PUAN = 0
        self.BOLUM_NO = 1
        self.oyuncu.CAN = 5
        #yeniden başlatma için grupları sıfırladık
        self.uzayli_grup.empty()
        self.uzayli_mermi_grup.empty()
        self.oyuncu_mermi_grup.empty()
        self.bolum() # yeniden başlattığımız için 1. bölüm ile ilgili bilgileri(uzaylı sayısı vb.) yeniden yüklememiz gerekiyor