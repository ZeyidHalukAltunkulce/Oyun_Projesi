import pygame


## Pencere boyutu
GENISLIK, YUKSEKLIK = 1280, 720

## oyunu meydana getiren karelerin hesaplanarak oluşturulması hızını, doğru bir akıcılık ile belirlememiz gerekiyor
FPS = 60  # (30/60/144)
saat = pygame.time.Clock()