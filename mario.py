import pygame
import sys
import os

# Inicializar o Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 1500, 800
GROUND_HEIGHT = 15
FPS = 60

# Cores
RED = (255, 0, 0)

# Caminhos relativos para as imagens de fundo
background_images = [
    pygame.image.load(os.path.join("images", "background1.jpeg")),
    pygame.image.load(os.path.join("images", "background.gif")),
    # Adicione mais imagens conforme necessário
]
current_background = 0
background_image = pygame.transform.scale(background_images[current_background], (WIDTH, HEIGHT))

# Gravidade e velocidade do jogador
gravity = 1

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load(os.path.join("images", "mario.png"))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.y_speed = 0

    def update(self):
        self.y_speed += gravity
        self.rect.y += self.y_speed

        # Verificar colisão com o chão
        if self.rect.bottom > HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.y_speed = 0

class Villain(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, image_path):
        super().__init__()
        self.image = pygame.image.load(os.path.join("images", "vilan.png"))

        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = speed
    def check_collision_with_player(self, player):
        return pygame.sprite.collide_rect(self, player)
    def update(self):
        self.rect.x += self.speed

        # Inverter a direção quando atingir as bordas da tela
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed = -self.speed

# Criar a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Game")

# Criar jogador
player = Player(WIDTH // 2, HEIGHT - GROUND_HEIGHT, 150, 150)

# Criar vilões
villain1 = Villain(100, HEIGHT - GROUND_HEIGHT, 150, 150, 5, "vilain_image1.png")
villain2 = Villain(400, HEIGHT - GROUND_HEIGHT, 150, 150, -3, "vilain_image2.png")

# Grupos de sprites para facilitar a atualização e desenho
all_sprites = pygame.sprite.Group()
all_sprites.add(player, villain1, villain2)

# Inicializar clock
clock = pygame.time.Clock()

# Loop do jogo
# Loop do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Movimento do jogador
    if keys[pygame.K_LEFT] and player.rect.left > 0:
        player.rect.x -= 5
    if keys[pygame.K_RIGHT] and player.rect.right < WIDTH:
        player.rect.x += 5

    # Salto do jogador
    if keys[pygame.K_SPACE] and player.rect.bottom == HEIGHT - GROUND_HEIGHT:
        player.y_speed = -30  # Ajuste conforme necessário para a altura do salto

    # Atualizar o jogador
    player.update()

    # Verificar colisão entre vilões e jogador
    for villain in [villain1, villain2]:
        if villain.check_collision_with_player(player):
            villain.speed = 0  # Parar o vilão se houver colisão

    # Atualizar os vilões
    villain1.update()
    villain2.update()

    # Verificar se o jogador atingiu o final da tela direita
    if player.rect.right >= WIDTH:
        # Trocar para o próximo plano de fundo
        current_background = (current_background + 1) % len(background_images)
        background_image = pygame.transform.scale(background_images[current_background], (WIDTH, HEIGHT))
        player.rect.x = 0  # Reiniciar a posição do jogador à esquerda

    # Atualizar o fundo
    screen.blit(background_image, (0, 0))

    # Desenhar todos os sprites
    all_sprites.draw(screen)

    # Atualizar a tela
    pygame.display.flip()

    # Controlar a taxa de quadros
    clock.tick(FPS)
