import sys
import os
import pygame
from classes import LevelChoiseMenuButton, ButtonBackLvlChoise, ButtonFirstLvl, load_image, ShopButton, ExitButton


def load_main_menu(fonts):
    background = load_image("background.png")
    background_show = pygame.transform.scale(background, (1920, 1080))
    screen_main_menu.blit(background_show, (0, 0))
    # Создание заднего фона главного меню


    buttons_main_menu.draw(buttons_screen_main_menu)  # Сначала рисуются кнопки


def load_level_choise():
    background = load_image("level_choise.png")
    background_show = pygame.transform.scale(background, (1920, 1080))
    screen_level_choise.blit(background_show, (0, 0))
    # Создание заднего фона меню выбора уровня

    buttons_level_choise.draw(buttons_screen_level_choise) # Отрисовка кнопок меню выбора уровня

if __name__ == '__main__':
    pygame.init()
    width, height = 1920, 1080
    size = width, height

    screen_main_menu = pygame.display.set_mode(size)  # Экран на который накладывается фон главного меню
    screen_level_choise = pygame.display.set_mode(size)  # Экран на который накладывается фон меню выбора уровня

    buttons_screen_main_menu = pygame.display.set_mode(size)  # Экран на который накладываются кнопки главного меню
    buttons_screen_level_choise = pygame.display.set_mode(size)  # Экран на который накладываются кнопки меню выбора уровня

    buttons_main_menu = pygame.sprite.Group()  # Создание группы со спрайтами кнопок в главном меню
    buttons_font = pygame.font.SysFont('serif_bold', 150)  # Создание переменной со шрифтом на кнопках в главном меню

    buttons_level_choise = pygame.sprite.Group()  # Создание группы со спрайтами кнопок меню выбора уровня

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

    while True:
        if main_menu_flag:
            load_main_menu(buttons_font)  # Функция загрузки главного меню
        if level_choise_flag:
            load_level_choise()  # Функция загрузки меню выбора уровней
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
                    print("Уровень первый")
                # Кнопка первого уровня в меню выбора уровней
        pygame.display.flip()