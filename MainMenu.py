import sys
import os
import pygame
import math
from classes import LevelChoiseMenuButton, ShopButton, ExitButton, ButtonBackLvlChoise, ButtonFirstLvl, load_image, \
    TowerCell, Player, SelectUpgradeMenu, FirstTower

FPS = 30


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

    buttons_level_choise = pygame.sprite.Group()  # Создание группы со спрайтами кнопок меню выбора уровня

    buttons_level1 = pygame.sprite.Group() # группа с кнопками из 1 уровня

    towers_group = pygame.sprite.Group() # Группа со спрайтами клеток

    really_tower_group = pygame.sprite.Group() # группа со спрайтами башен

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

    tower1 = FirstTower(really_tower_group)

    back_button_level_choise = ButtonBackLvlChoise(buttons_level_choise)  # Кнопка "назад"
    first_lvl_button = ButtonFirstLvl(buttons_level_choise)  # Кнопка первого уровня
    # Создание кнопок в меню выбора уровня

    level_choise_flag = False  # Если этот флаг активен, будет загружаться меню выбора уровня
    main_menu_flag = True  # Если этот флаг активен, будет загружаться главное меню
    first_lvl_start = False


    secret_important_number = 0

    red = (255, 0, 0)
    yellow = (255, 255, 0)

    towers = [] # список поставленных башен


    class Tower:
        def __init__(self, x, y,  damage, cd, price, radius):
            self.x = x
            self.y = y
            self.damage = damage
            self.fire_rate = cd
            self.fire_rate_tick = 0
            self.price = price
            self.radius = radius

        def Draw(self, window):
            really_tower_group.draw(first_level_screen)


    def tower_place():
        print(1)
        if secret_important_number == 26:
            print(secret_important_number)
            really_tower_group.draw(first_level_screen)
            tower1.change_rect(1086, 960)
        pos = pygame.mouse.get_pos()
        pos_x = math.floor(pos[0] / 128) * 128 #  128 - размер одной клеточки
        pos_y = math.floor(pos[1] / 128) * 128
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            print(123)
            towers.append(Tower(1086, 960, 10,  0.5, 300, 150))
            player.money -= 10

    generate_level(load_level("1map.txt"))
    player = Player(100, 10)
    f2 = pygame.font.SysFont('comic sans', 66)
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
            tower_select_menu = SelectUpgradeMenu(buttons_level1)
            buttons_level1.draw(first_level_screen)


            money = f2.render(str(player.money), False, yellow)
            health = f2.render(str(player.health), False, red)

            money_text = f2.render(("Монеты:"), False, yellow)
            health_text = f2.render(("Жизни:"), False, red)
            first_level_screen.blit(money, (1300, 20))
            first_level_screen.blit(health, (700, 20))
            first_level_screen.blit(money_text, (1020, 20))
            first_level_screen.blit(health_text, (470, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Обработка нажатия на кнопку
                x, y = event.pos
                if buttons_main_menu.sprites()[0].rect.collidepoint(x, y) and main_menu_flag:
                    level_choise_flag = True
                    main_menu_flag = False
                # Кнопка "начать игру" в главном меню
                elif buttons_main_menu.sprites()[1].rect.collidepoint(x, y):
                    store_button.update()
                # Кнопка магазина в главном меню
                elif buttons_main_menu.sprites()[2].rect.collidepoint(x, y) and main_menu_flag:
                    sys.exit()
                # Кнопка выхода на рабочий стол в главном меню
                elif buttons_level_choise.sprites()[0].rect.collidepoint(x, y) and level_choise_flag:
                    level_choise_flag = False
                    main_menu_flag = True
                # Кнопка "Назад" в меню выбора уровня
                elif buttons_level_choise.sprites()[1].rect.collidepoint(x, y) and level_choise_flag:
                    first_lvl_start = True
                    level_choise_flag = False
                # Кнопка первого уровня в меню выбора уровней
                elif first_lvl_start:
                    for i in range(0, 26):  # всего 26 клеточек на 1 карте
                        if towers_group.sprites()[i].rect.collidepoint(x, y) and first_level_screen:
                            print(i) # печатает номер выбранной клеточки
                            secret_important_number = i # запоминает выбранную клеточку
                            tower_place()
                            for tower in towers:
                                tower.Draw(first_level_screen)

        pygame.display.flip()
