import sys
import os
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button(pygame.sprite.Sprite):
    image = load_image("button.png")
    image_clicked = load_image("button_clicked.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Button.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def change_rect(self, x, y):  # Смена положения спрайта
        self.rect.x = x
        self.rect.y = y

    def update(self):  # В программе функция вызывается при нажатии на спрайт
        self.image = Button.image_clicked

if __name__ == '__main__':
    pygame.init()
    width, height = 1920, 1025
    size = width, height
    screen = pygame.display.set_mode(size)  # Основной экран
    buttons_screen = pygame.display.set_mode(size) # Экран с кнопками и текстом на них

    background = load_image("background.png")
    background_show = pygame.transform.scale(background, (1920, 1025))
    screen.blit(background_show, (0, 0))
    # Создание заднего фона

    font = pygame.font.SysFont('serif', 100)
    title = font.render("TowerDefence", True, (10, 10, 10))
    screen.blit(title, (680, 50))
    # Создание титульного текста

    buttons = pygame.sprite.Group()  # Создание группы со спрайтами кнопок
    buttons_font = pygame.font.SysFont('serif_bold', 70)  # Создание переменной со шрифтом на кнопках

    start_game_button = Button(buttons)
    start_game_button.change_rect(670, 350)
    # Создание кнопки начала игры (выбора уровня)

    store_button = Button(buttons)
    store_button.change_rect(670, 550)
    # Создание кнопки магазина

    start_game_text = buttons_font.render("Начать игру", True, (10, 10, 10))
    store_text = buttons_font.render("Магазин", True, (10, 10, 10))
    # Создание текста на кнопках
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Обработка нажатия на кнопку
                x, y = event.pos
                if buttons.sprites()[0].rect.collidepoint(x, y):
                    print("Начать игру")
                    start_game_button.update()
                if buttons.sprites()[1].rect.collidepoint(x, y):
                    print("Магазин")
                    store_button.update()

        buttons.draw(buttons_screen)  # Сначала рисуются кнопки
        buttons_screen.blit(start_game_text, (830, 400))
        buttons_screen.blit(store_text, (870, 600)) # Затем текст на них
        pygame.display.flip()
