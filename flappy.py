import pygame, random
from pygame.locals import*
from sys import exit
import os

pygame.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal,'Assets')

LARGURA_TELA = 1140
ALTURA_TELA = 724
VELOCIDADE = 17
GRAVIDADE = 1
VELOCIDADE_JOGO = 10

LARGURA_CHAO = 2 * LARGURA_TELA 
ALTURA_CHAO = 100

LARGURA_CANO = 100
ALTURA_CANO = 450
CANO_GAP = -330 

tela = pygame.display.set_mode((LARGURA_TELA,ALTURA_TELA))
pygame.display.set_caption("The Best Hero")
fps = pygame.time.Clock()


IMAGEM_FUNDO = pygame.image.load(os.path.join(diretorio_imagens,'cenario3.png')).convert_alpha()
IMAGEM_FUNDO = pygame.transform.scale(IMAGEM_FUNDO,(1140,724))

class Chao(pygame.sprite.Sprite):
    def __init__(self,x_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(diretorio_imagens,'chão.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(LARGURA_CHAO, ALTURA_CHAO))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = x_pos
        self.rect[1] = ALTURA_TELA - ALTURA_CHAO
    def update(self):
        self.rect[0] -= VELOCIDADE_JOGO

class Cano(pygame.sprite.Sprite):
    def __init__(self, invertido, x_pos, y_tamanho):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(diretorio_imagens,'cano1.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(LARGURA_CANO,ALTURA_CANO))
        self.rect = self.image.get_rect()
        self.rect[0] = x_pos
        if invertido:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = (self.rect[3] - y_tamanho)
        else:
            self.rect[1] = ALTURA_TELA - y_tamanho
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect[0] -= VELOCIDADE_JOGO

class Heroi(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_heroi = []
        sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens,'aviao_sprite_sheet.png')).convert_alpha()
        
        for i in range (6):
            img = sprite_sheet.subsurface((i * 200.5,0),(200.5,135))
            img = pygame.transform.scale(img,(125,95))
            self.imagens_heroi.append(img)
            
        self.velocidade = VELOCIDADE
        self.playerX = 200
        self.playerY = 0
        self.index_lista = 0
        self.image = self.imagens_heroi[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (self.playerX,self.playerY)

    def update(self):
        if self.index_lista > 5.90:
            self.index_lista = 0
        self.index_lista += 0.22
        self.image = self.imagens_heroi[int(self.index_lista)]
        self.velocidade += GRAVIDADE
        self.playerY += self.velocidade
        self.rect.center = (self.playerX, self.playerY)

    def voar(self):
        self.velocidade = -VELOCIDADE

def fora_da_tela(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def canos_aleatorios(x_pos):
    tamanho = random.randint(200, 350)
    cano = Cano(False, x_pos, tamanho)
    cano_invertido = Cano(True, x_pos, ALTURA_TELA - tamanho - CANO_GAP)
    return (cano, cano_invertido)

grupo_heroi = pygame.sprite.Group()
heroi = Heroi()
grupo_heroi.add(heroi)

grupo_chao = pygame.sprite.Group()
for i in range(2):
    chao = Chao(LARGURA_CHAO * i)
    grupo_chao.add(chao)

grupo_cano = pygame.sprite.Group()
for i in range (2):
    canos = canos_aleatorios(LARGURA_TELA * i + 800)
    grupo_cano.add(canos[0])
    grupo_cano.add(canos[1]) 


while True:
    fps.tick(55)
    tela.blit(IMAGEM_FUNDO,(0,0))
    grupo_heroi.draw(tela)
    grupo_cano.draw(tela)
    grupo_chao.draw(tela)
    

    for event in pygame.event.get():    
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                heroi.voar()
    if fora_da_tela(grupo_chao.sprites()[0]):
        grupo_chao.remove(grupo_chao.sprites()[0])
        novo_chao = Chao(LARGURA_CHAO - 20)
        grupo_chao.add(novo_chao)

    if fora_da_tela(grupo_cano.sprites()[0]):
        grupo_cano.remove(grupo_cano.sprites()[0])
        grupo_cano.remove(grupo_cano.sprites()[0])
        canos = canos_aleatorios(LARGURA_TELA * 2)
        grupo_cano.add(canos[0]) 
        grupo_cano.add(canos[1]) 
        
    if pygame.sprite.groupcollide(grupo_heroi, grupo_chao, False, False, pygame.sprite.collide_mask):
        break
    if pygame.sprite.groupcollide(grupo_heroi, grupo_cano, False, False, pygame.sprite.collide_mask):
        break 

    grupo_cano.update()
    grupo_heroi.update()
    grupo_chao.update()
    pygame.display.flip()