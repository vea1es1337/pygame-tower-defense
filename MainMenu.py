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


def load_main_menu(group, fonts):
    background = load_image("background.png")
    background_show = pygame.transform.scale(background, (1920, 1025))
    screen_main_menu.blit(background_show, (0, 0))
    # Создание заднего фона

    font = pygame.font.SysFont('serif', 100)
    title = font.render("TowerDefence", True, (10, 10, 10))
    screen_main_menu.blit(title, (680, 50))
    # Создание титульного текста

    start_game_text = fonts.render("Начать игру", True, (10, 10, 10))
    store_text = fonts.render("Магазин", True, (10, 10, 10))
    # Создание текста на кнопках

    buttons_main_menu.draw(buttons_screen_main_menu)  # Сначала рисуются кнопки
    buttons_screen_main_menu.blit(start_game_text, (830, 400))
    buttons_screen_main_menu.blit(store_text, (870, 600))  # Затем текст на них


def load_level_choise():
    background = load_image("level_choise.png")
    background_show = pygame.transform.scale(background, (1920, 1025))
    screen_level_choise.blit(background_show, (0, 0))

    buttons_level_choise.draw(buttons_screen_level_choise)


class ButtonBackLvlChoise(pygame.sprite.Sprite):
    image = load_image("level_choise_back_btn.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonBackLvlChoise.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def change_rect(self, x, y):
        self.rect.x = x
        self.rect.y = y

class ButtonLvlChoise(pygame.sprite.Sprite):
    pass


class ButtonMainMenu(pygame.sprite.Sprite):
    image = load_image("button.png")
    image_clicked = load_image("button_clicked.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonMainMenu.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def change_rect(self, x, y):  # Смена положения спрайта
        self.rect.x = x
        self.rect.y = y

    def update(self):  # В программе функция вызывается при нажатии на спрайт
        self.image = ButtonMainMenu.image_clicked


if __name__ == '__main__':
    pygame.init()
    width, height = 1920, 1025
    size = width, height

    screen_main_menu = pygame.display.set_mode(size)  # Основной экран
    screen_level_choise = pygame.display.set_mode(size)

    buttons_screen_main_menu = pygame.display.set_mode(size)
    buttons_screen_level_choise = pygame.display.set_mode(size)

    buttons_main_menu = pygame.sprite.Group()  # Создание группы со спрайтами кнопок
    buttons_font = pygame.font.SysFont('serif_bold', 70)  # Создание переменной со шрифтом на кнопках

    buttons_level_choise = pygame.sprite.Group()

    start_game_button = ButtonMainMenu(buttons_main_menu)
    start_game_button.change_rect(670, 350)
    # Создание кнопки начала игры (выбора уровня)

    store_button = ButtonMainMenu(buttons_main_menu)
    store_button.change_rect(670, 550)
    # Создание кнопки магазина

    back_button_level_choise = ButtonBackLvlChoise(buttons_level_choise)
    back_button_level_choise.change_rect(1126, 40)

    level_choise_flag = False
    main_menu_flag = True

    while True:
        if main_menu_flag:
            load_main_menu(buttons_main_menu, buttons_font)
        if level_choise_flag:
            load_level_choise()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Обработка нажатия на кнопку
                x, y = event.pos
                if buttons_main_menu.sprites()[0].rect.collidepoint(x, y) and main_menu_flag:
                    level_choise_flag = True
                    main_menu_flag = False
                if buttons_main_menu.sprites()[1].rect.collidepoint(x, y):
                    store_button.update()
                if buttons_level_choise.sprites()[0].rect.collidepoint(x, y) and level_choise_flag:
                    level_choise_flag = False
                    main_menu_flag = True

        pygame.display.flip()
