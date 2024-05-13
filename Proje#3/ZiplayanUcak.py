import pygame as pg
import random, sys

pg.init()

def zemin_yerlestir():
    ekran.blit(zemin,(zemin_x_poz,450))
    ekran.blit(zemin,(zemin_x_poz+288,450))

def ucagi_dondur(ucak):
    yeni_ucak = pg.transform.rotozoom(ucak,-ivme*5,1.15) # Uçağı döndürme fonksiyonu
    return yeni_ucak

def ucak_animasyon():
    yeni_ucak = ucak_listesi[ucak_numarasi]
    yeni_ucak_dortgeni = ucak_yuzeyi.get_rect(center = (50,ucak_dortgeni.centery))
    return yeni_ucak,yeni_ucak_dortgeni

def boru_yarat(artik_yol):
    rastgele_boru_poz = random.choice(boru_yuksekligi)
    alt_boru = boru_yuzeyi.get_rect(midtop = (350+artik_yol,rastgele_boru_poz))
    ust_boru = boru_yuzeyi.get_rect(midbottom = (350+artik_yol,rastgele_boru_poz - 150))
    return alt_boru,ust_boru

def borulari_yerlestir(borular):
    for boru in borular:
        if boru.bottom >= 512:
            ekran.blit(boru_yuzeyi,boru)

        else:
            boruyu_dondur = pg.transform.flip(boru_yuzeyi,False,True)
            ekran.blit(boruyu_dondur,boru)

def borulari_tasi(borular):
    for boru in borular:
        boru.centerx -= 3
    return borular

def carpisma_kontrolu(borular):
    for boru in borular:
        if ucak_dortgeni.colliderect(boru):
            olme_efekti.play()
            return False
        if ucak_dortgeni.top <= -50 or ucak_dortgeni.bottom >= 450:
            return False
    return True

def rekoru_guncelle(skor,rekor):
    if skor > rekor:
        rekor = skor
    return rekor

def skoru_goster(oyun_durumu):
    if oyun_durumu == "oyun_bitti":
        if skor < 0:
            skor_yuzeyi = yazi_tipi.render(f'SKOR: {int(0)}',True,(255,255,255))
        if skor > 0:
            skor_yuzeyi = yazi_tipi.render(f'SKOR: {int(skor)}',True,(0,0,80))
        skor_dortgeni = skor_yuzeyi.get_rect(center = (144,50))
        ekran.blit(skor_yuzeyi,skor_dortgeni)

        rekor_yuzeyi = yazi_tipi.render(f'REKOR: {int(rekor)}',True,(55,245,125))
        rekor_dortgeni = rekor_yuzeyi.get_rect(center = (144,450))
        ekran.blit(rekor_yuzeyi,rekor_dortgeni)

    if oyun_durumu == "ana_oyun":
        if skor < 0:
            skor_yuzeyi = yazi_tipi.render(f'SKOR: {int(0)}',True,(255,255,255))
        if skor > 0:
            skor_yuzeyi = yazi_tipi.render(f'SKOR: {int(skor)}',True,(255,255,255))

        skor_dortgeni = skor_yuzeyi.get_rect(center = (144,50))
        ekran.blit(skor_yuzeyi,skor_dortgeni)


ekran = pg.display.set_mode((288,512))
zaman = pg.time.Clock()

pg.display.set_caption("Zıplayan Uçak")
ikon = pg.image.load("Uçak_düz.png")
pg.display.set_icon(ikon)

arkaplan_yuzeyi = pg.image.load("arkaplan.png")
zemin = pg.image.load("yer.png")

ucak_duz = pg.image.load("Uçak_düz.png")
ucak_ortada = pg.image.load("Uçak_ileri.png")
ucak_ters = pg.image.load("Uçak_bozulmuş.png")
ucak_numarasi = 0
ucak_listesi = [ucak_duz,ucak_ortada,ucak_ters]
ucak_yuzeyi = ucak_listesi[ucak_numarasi]
ucak_dortgeni = ucak_yuzeyi.get_rect(center = (50,256))
yercekimi = 0.125  # ivme
ivme = 0

yazi_tipi = pg.font.Font("04B_19.TTF",40)

boru_yuzeyi = pg.image.load("kırmızı_boru.png")
boru_listesi = []
BORU_URET = pg.USEREVENT + 0
pg.time.set_timer(BORU_URET,1200)
boru_yuksekligi = [200,250,300,350,400]

zemin_x_poz = 0

UCAK_DONDUR = pg.USEREVENT + 1
pg.time.set_timer(UCAK_DONDUR,150) # Her 150 ms de bir dönsün.

oyun_bitti_yuzeyi = pg.image.load("başlangıç.png")
oyun_bitti_dortgeni = oyun_bitti_yuzeyi.get_rect(center = (110,170))
oyun_bitti_yuzeyi = pg.transform.rotozoom(oyun_bitti_yuzeyi,0,1.4)

oyun_aktif = True
skor = -1.388888889
rekor = 0
artik_yol = 0

ziplama = pg.mixer.Sound("uçma.ogg")
olme_efekti = pg.mixer.Sound("çarpma.wav")

while True:
    for olay in pg.event.get():
        if olay.type == pg.QUIT: 
            pg.quit()
            sys.exit()

        if olay.type == pg.KEYDOWN:
            if olay.key == pg.K_SPACE and oyun_aktif == True:
                ivme = -5
                ziplama.play()

            if olay.key == pg.K_SPACE and oyun_aktif == False:
                oyun_aktif = True
                boru_listesi.clear()
                ucak_dortgeni.center = (50,256)
                ucak_net_ivmesi = 0
                artik_zaman = pg.time.get_ticks()%1200
                artik_yol = 60*(artik_zaman/1000)*3
                skor = -1.388888889


        if olay.type == UCAK_DONDUR:
            if ucak_numarasi < 2:
                ucak_numarasi += 1
            else :
                ucak_numarasi = 0
            ucak_yuzeyi, ucak_dortgeni = ucak_animasyon()

        if olay.type == BORU_URET:
            boru_listesi.extend(boru_yarat(artik_yol))

    ekran.blit(arkaplan_yuzeyi,(0,0))

    if oyun_aktif:
        oyun_aktif = carpisma_kontrolu(boru_listesi)
        boru_listesi = borulari_tasi(boru_listesi)
        borulari_yerlestir((boru_listesi))

        # Uygulanan net ivme
        ivme += yercekimi
        donmus_ucak = ucagi_dondur(ucak_yuzeyi)
        ucak_dortgeni.centery += ivme
        ekran.blit(donmus_ucak,ucak_dortgeni)
        skor += 0.01388888889
        skoru_goster("ana_oyun")

    else :
        ekran.blit(oyun_bitti_yuzeyi,oyun_bitti_dortgeni)
        rekor = rekoru_guncelle(skor,rekor)
        skoru_goster("oyun_bitti")

    #zemin
    zemin_x_poz -= 3
    zemin_yerlestir()

    if zemin_x_poz <= -288:
        zemin_x_poz = 0

    pg.display.update()
    zaman.tick(60)  