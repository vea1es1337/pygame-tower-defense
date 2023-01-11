import sys
import os
import pygame
from classes import LevelChoiseMenuButton, ShopButton, ExitButton, ButtonBackLvlChoise, ButtonFirstLvl, load_image, \
    TowerCell


def load_main_menu():
    background = load_image("background.png")
    background_show = pygame.transform.scale(background, (1920, 1080))
    screen_main_menu.blit(background_show, (0, 0))
    # Создание заднего фона главного меню
    buttons_main_menu.draw(buttons_screen_main_menu)  # Отрисовка кнопок


def load_level_choise_menu():
    background = load_image("level_choise.png")
    background_show = pygame.transform.scale(background, (1920, 1080))
    screen_level_choise.blit(background_show, (0, 0))
    # Создание заднего фона меню выбора уровня
    buttons_level_choise.draw(buttons_screen_level_choise)  # Отрисовка кнопок меню выбора уровня


def load_level(filename):  # Функция возвращает текстовый файл башен уровня 1
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        for x in range(len(level_map)):
            level_map[x] = list(level_map[x])
    return level_map


def generate_level(level):  # Генерация уровня 1
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                TowerCell(x, y, towers_group)


if __name__ == '__main__':
    pygame.init()
    width, height = 1920, 1080
    size = width, height

    screen_main_menu = pygame.display.set_mode(size)  # Экран на который накладывается фон главного меню
    screen_level_choise = pygame.display.set_mode(size)  # Экран на который накладывается фон меню выбора уровня

    buttons_screen_main_menu = pygame.display.set_mode(size)  # Экран на который накладываются кнопки главного меню
    buttons_screen_level_choise = pygame.display.set_mode(
        size)  # Экран на который накладываются кнопки меню выбора уровня

    buttons_main_menu = pygame.sprite.Group()  # Создание группы со спрайтами кнопок в главном меню
    buttons_font = pygame.font.SysFont('serif_bold', 150)  # Создание переменной со шрифтом на кнопках в главном меню

    buttons_level_choise = pygame.sprite.Group()  # Создание группы со спрайтами кнопок меню выбора уровня

    towers_group = pygame.sprite.Group() # Группа со спрайтами башен
    first_level_screen = pygame.display.set_mode(size) # Экран, на котором рисуется первый уровень

    start_game_button = LevelChoiseMenuButton(buttons_main_menu)
    start_game_button.change_rect(1170, 670)
    # Создание кнопки начала игры (выбора уровня) в главном меню

    store_button = ShopButton(buttons_main_menu)
    store_button.change_rect(100, 670)
    # Создание кнопки магазина в главном меню

    exit_button_main_menu = ExitButton(buttons_main_menu)
    exit_button_main_menu.change_rect(1600, 150)
    # Создание кнопки выхода из игры в главном меню

    back_button_level_choise = ButtonBackLvlChoise(buttons_level_choise)  # Кнопка "назад"
    first_lvl_button = ButtonFirstLvl(buttons_level_choise)  # Кнопка первого уровня
    # Создание кнопок в меню выбора уровня

    level_choise_flag = False  # Если этот флаг активен, будет загружаться меню выбора уровня
    main_menu_flag = True  # Если этот флаг активен, будет загружаться главное меню
    first_lvl_start = False

    for x in load_level("1map.txt"):
        print(x)

    generate_level(load_level("1map.txt"))

    while True:
        if main_menu_flag:
            load_main_menu()  # Функция загрузки главного меню
        if level_choise_flag:
            load_level_choise_menu()  # Функция загрузки меню выбора уровней
        if first_lvl_start:
            background = load_image("first_map.png")
            background_show = pygame.transform.scale(background, (1920, 1080))
            first_level_screen.blit(background_show, (0, 0))
            towers_group.draw(first_level_screen)  # Отрисовка карты первого уровня

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Обработка нажатия на кнопку
                x, y = event.pos
                if buttons_main_menu.sprites()[0].rect.collidepoint(x, y) and main_menu_flag:
                    level_choise_flag = True
                    main_menu_flag = False
                # Кнопка "начать игру" в главном меню
                if buttons_main_menu.sprites()[1].rect.collidepoint(x, y):
                    store_button.update()
                # Кнопка магазина в главном меню
                if buttons_main_menu.sprites()[2].rect.collidepoint(x, y) and main_menu_flag:
                    sys.exit()
                # Кнопка выхода на рабочий стол в главном меню
                if buttons_level_choise.sprites()[0].rect.collidepoint(x, y) and level_choise_flag:
                    level_choise_flag = False
                    main_menu_flag = True
                # Кнопка "Назад" в меню выбора уровня
                if buttons_level_choise.sprites()[1].rect.collidepoint(x, y) and level_choise_flag:
                    first_lvl_start = True
                    level_choise_flag = False
                # Кнопка первого уровня в меню выбора уровней
                if towers_group.sprites()[-1].rect.collidepoint(x, y) and first_level_screen:
                    first_lvl_start = False
                    level_choise_flag = True
                # Нажатие на последнюю башню (Дима исправь)
        pygame.display.flip()
