import sys
import os
import threading
import time

import pygame
import math
from classes import LevelChoiseMenuButton, ShopButton, ExitButton, ButtonBackLvlChoise, ButtonFirstLvl, load_image, \
    TowerCell, Player, SelectUpgradeMenu




clock = pygame.time.Clock()
FPS = 25

def load_main_menu():
    background = load_image("background.png").convert_alpha()
    background_show = pygame.transform.scale(background, (1920, 1080))
    screen_main_menu.blit(background_show, (0, 0))
    # Создание заднего фона главного меню
    buttons_main_menu.draw(buttons_screen_main_menu)  # Отрисовка кнопок


def load_level_choise_menu():
    background = load_image("level_choise.png").convert_alpha()
    background_show = pygame.transform.scale(background, (1920, 1080))
    screen_level_choise.blit(background_show, (0, 0))
    # Создание заднего фона меню выбора уровня
    buttons_level_choise.draw(buttons_screen_level_choise)  # Отрисовка кнопок меню выбора уровня

def load_first_level():
    background = load_image("first_map.png").convert_alpha()
    background_show = pygame.transform.scale(background, (1920, 1080))
    first_level_screen.blit(background_show, (0, 0))
    towers_group.draw(first_level_screen)  # Отрисовка карты первого уровня

    buttons_level1.draw(buttons_screen_level)


def load_level(filename):  # Функция возвращает текстовый файл клеток уровня 1
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
    buttons_screen_level = pygame.display.set_mode(  # Экран на который накладываются кнопки из уровня
size)

    buttons_main_menu = pygame.sprite.Group()  # Создание группы со спрайтами кнопок в главном меню

    buttons_level_choise = pygame.sprite.Group()  # Создание группы со спрайтами кнопок меню выбора уровня

    buttons_level1 = pygame.sprite.Group() # группа с кнопками из 1 уровня

    towers_group = pygame.sprite.Group() # Группа со спрайтами клеток

    really_tower_group = pygame.sprite.Group() # группа спрайтика первой башни
    first_enemy_group = pygame.sprite.Group() # группа спрата первого врага

    tower1 = pygame.sprite.Sprite()
    tower1.image = load_image("common_lvl1.png").convert_alpha()
    tower1.rect = tower1.image.get_rect()
    really_tower_group.add(tower1)

    enemy1 = pygame.sprite.Sprite()
    enemy1.image = load_image("enemy1.png").convert_alpha()
    enemy1.rect = tower1.image.get_rect()
    first_enemy_group.add(enemy1)

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
    tower_select_menu = SelectUpgradeMenu(buttons_level1)

    level_choise_flag = False  # Если этот флаг активен, будет загружаться меню выбора уровня
    main_menu_flag = True  # Если этот флаг активен, будет загружаться главное меню
    first_lvl_start = False



    red = (255, 0, 0)
    yellow = (255, 255, 0)
    cyan = (20, 175, 255)
    cells_flag = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                  ] # флаг активированных клеток
    towers = [] # список поставленных башен
    shapes = [] # список текущих на экране врагов
    bullets = [] # список текущих на экране пуль
    shapes_way = [] # список из клеток путя врагов
    way_points = [] # список точек на карте, к которым они должны идти(чтобы вручную весь путь не рисовать)
    player = Player(9000, 10) # у игрока 350 монет и 10 жизней


    def create_shapes_way(level): # создаёт пути, по которому идут враги
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == "#":
                    shapes_way.append([x * 128, y * 128, 128, 128, ])  # добавляется по каждой клетке путь врага
        print(shapes_way)


    def сreate_way_points(level, points):
        point = "1"
        int_point = 1
        for i in range(points):
            for y in range(len(level)):
                for x in range(len(level[0])):
                    if level[y][x] == point:
                        way_points.append([x * 128 + 64 // 2, y * 128 + 64 // 2, 10, 10])
                        int_point += 1
                        point = str(int_point)
        print(way_points)
    def draw_shapes_way():
        for way in shapes_way:
            pygame.draw.rect(first_level_screen, yellow, way)

    class Tower1:
        def __init__(self, x, y,  damage, cd,  price, range):
            self.x = x
            self.y = y
            self.damage = damage
            self.firerate = cd # время перезарядки
            self.firerate_tick = 0 # выступает в качестве таймера для firerate
            self.price = price
            self.range = range

        def Draw(self):
            tower1.rect.x = self.x
            tower1.rect.y = self.y
            really_tower_group.draw(first_level_screen)

        def shooting(self):
            if self.firerate_tick <= 0:
                creating_bullets(self.x, self.y, cyan, 15, 1, 25)
                self.firerate_tick = self.firerate
            else:
                self.firerate_tick -= 1 / FPS

    class Bullet: # создание класса пули
        def __init__(self, x, y, color, size, dmg, speed):
            self.x = x
            self.y = y
            self.size = size
            self.color = color
            self.dmg = dmg
            self.speed = speed

        def move(self, vec_x, vec_y):  # функция движения пули, принимающая в аргументы векторные x и y
            self.x += self.speed * vec_x
            self.y += self.speed * vec_y

        def Draw(self):
            pygame.draw.circle(first_level_screen, self.color, [self.x, self.y], self.size)


    class Shape1:               # класс врага первого
        def __init__(self, x, y, hp, speed, reward):
            self.x = x
            self.y = y
            self.speed = speed
            self.point = 0
            self.reward = reward
            self.hp = hp

        def Draw(self):
            enemy1.rect.x = self.x
            enemy1.rect.y = self.y
            first_enemy_group.draw(first_level_screen)

        def Move(self):  # для движения умножаем значения векторов на скорость и прибавлять его к координатам
            move = homing_calculation(self.x, self.y, way_points[self.point][0], way_points[self.point][1])
            self.x += self.speed * move[0]
            self.y += self.speed * move[1]
            if move[2] <= self.speed:
                self.point += 1
                if self.point == len(way_points):
                    shapes.remove(self)
                    player.health -= 1


    def homing_calculation(x1, y1, x2,
                           y2):  # самонаведение снарядов с использованием линейной алгебры и немного геометрии,
        # нашёл это самонаводение в интернете для своего кода
        vec_x = x2 - x1
        vec_y = y2 - y1
        dist = math.sqrt(vec_x ** 2 + vec_y ** 2)  # расстояние между 2 объектами по теореме пифагора
        norm_vec_x = vec_x / dist  # нормализация вектора
        norm_vec_y = vec_y / dist  # нормализация вектора
        angle = math.atan2(norm_vec_y, norm_vec_x)  # угол
        return norm_vec_x, norm_vec_y, dist, angle


    # --------------------------- Следующая функция ставит башни на клетки. Из за спрайтов и моего не полного
    # клеточного поля, которое трогает только клетки, никаких других
    # выходов после поисков я не нашёл, это можно сделать только через if-ы

    def creating_tower():
        keys = pygame.key.get_pressed()
        x, y = pygame.mouse.get_pos()
        if towers_group.sprites()[26].rect.collidepoint(x, y):
            if cells_flag[26] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[26] = 1
                player.money -= 300
                towers.append(Tower1(1024, 896, 10, 1.5, 300, 150))
                print(26)
        if towers_group.sprites()[25].rect.collidepoint(x, y):
            if cells_flag[25] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[25] = 1
                player.money -= 300
                towers.append(Tower1(896, 896, 10, 1.5, 300, 150))
                print(25)
        if towers_group.sprites()[24].rect.collidepoint(x, y):
            if cells_flag[24] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[24] = 1
                player.money -= 300
                towers.append(Tower1(640, 896, 10, 1.5, 300, 150))
                print(24)
        if towers_group.sprites()[23].rect.collidepoint(x, y):
            if cells_flag[23] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                print(23)
                cells_flag[23] = 1
                player.money -= 300
                towers.append(Tower1(384, 896, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[22].rect.collidepoint(x, y):
            if cells_flag[22] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[22] = 1
                print(22)
                player.money -= 300
                towers.append(Tower1(128, 896, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[21].rect.collidepoint(x, y):
            if cells_flag[21] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[21] = 1
                print(21)
                player.money -= 300
                towers.append(Tower1(0, 768, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[20].rect.collidepoint(x, y):
            if cells_flag[20] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[20] = 1
                print(20)
                player.money -= 300
                towers.append(Tower1(896, 640, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[19].rect.collidepoint(x, y):
            if cells_flag[19] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[19] = 1
                print(19)
                player.money -= 300
                towers.append(Tower1(384, 640, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[18].rect.collidepoint(x, y):
            if cells_flag[18] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[18] = 1
                print(18)
                player.money -= 300
                towers.append(Tower1(256, 640, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[17].rect.collidepoint(x, y):
            if cells_flag[17] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[17] = 1
                print(17)
                player.money -= 300
                towers.append(Tower1(0, 640, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[16].rect.collidepoint(x, y):
            if cells_flag[16] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[16] = 1
                print(16)
                player.money -= 300
                towers.append(Tower1(1152, 512, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[15].rect.collidepoint(x, y):
            if cells_flag[15] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[15] = 1
                print(15)
                player.money -= 300
                towers.append(Tower1(896, 512, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[14].rect.collidepoint(x, y):
            if cells_flag[14] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[14] = 1
                print(14)
                player.money -= 300
                towers.append(Tower1(512, 512, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[13].rect.collidepoint(x, y):
            if cells_flag[13] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[13] = 1
                print(13)
                player.money -= 300
                towers.append(Tower1(256, 512, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[12].rect.collidepoint(x, y):
            if cells_flag[12] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[12] = 1
                print(12)
                player.money -= 300
                towers.append(Tower1(0, 512, 10, 1.5, 300, 150))
                print(towers)
        if towers_group.sprites()[11].rect.collidepoint(x, y):
            if cells_flag[11] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[11] = 1
                print(11)
                player.money -= 300
                towers.append(Tower1(896, 384, 10, 1.5, 300, 150))
        if towers_group.sprites()[10].rect.collidepoint(x, y):
            if cells_flag[10] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[10] = 1
                print(10)
                player.money -= 300
                towers.append(Tower1(512, 384, 10, 1.5, 300, 150))
        if towers_group.sprites()[9].rect.collidepoint(x, y):
            if cells_flag[9] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[9] = 1
                print(9)
                player.money -= 300
                towers.append(Tower1(256, 384, 10, 1.5, 300, 150))
        if towers_group.sprites()[8].rect.collidepoint(x, y):
            if cells_flag[8] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[8] = 1
                print(8)
                player.money -= 300
                towers.append(Tower1(0, 384, 10, 1.5, 300, 150))
        if towers_group.sprites()[7].rect.collidepoint(x, y):
            if cells_flag[7] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[7] = 1
                print(7)
                player.money -= 300
                towers.append(Tower1(256, 256, 10, 1.5, 300, 150))
        if towers_group.sprites()[6].rect.collidepoint(x, y):
            if cells_flag[6] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[6] = 1
                print(6)
                player.money -= 300
                towers.append(Tower1(0, 256, 10, 1.5, 300, 150))
        if towers_group.sprites()[5].rect.collidepoint(x, y):
            if cells_flag[5] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[5] = 1
                print(5)
                player.money -= 300
                towers.append(Tower1(1024, 128, 10, 1.5, 300, 150))
        if towers_group.sprites()[4].rect.collidepoint(x, y):
            if cells_flag[4] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[4] = 1
                print(4)
                player.money -= 300
                towers.append(Tower1(896, 128, 10, 1.5, 300, 150))
        if towers_group.sprites()[3].rect.collidepoint(x, y):
            if cells_flag[3] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[3] = 1
                print(3)
                player.money -= 300
                towers.append(Tower1(768, 128, 10, 1.5, 300, 150))
        if towers_group.sprites()[2].rect.collidepoint(x, y):
            if cells_flag[2] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[2] = 1
                print(2)
                player.money -= 300
                towers.append(Tower1(512, 128, 10, 1.5, 300, 150))
        if towers_group.sprites()[1].rect.collidepoint(x, y):
            if cells_flag[1] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[1] = 1
                print(1)
                player.money -= 300
                towers.append(Tower1(256, 128, 10, 1.5, 300, 150))
        if towers_group.sprites()[0].rect.collidepoint(x, y):
            if cells_flag[0] != 1 and keys[pygame.K_1] and player.money - 300 >= 0:
                cells_flag[0] = 1
                player.money -= 300
                towers.append(Tower1(0, 128, 10, 1.5, 300, 150))


# ---------------------------------------------------------------------
    # функция создания врагов


    def creating_enemys():
        for i in range(30, 1, -1):
            shapes.append(Shape1(160, (1 * i) * 16, 3, 6, 40))


    def creating_bullets(x, y, color, size, dmg, speed):
        bullets.append(Bullet(x, y, color, size, dmg, speed))

    def if_shape_died():
        for shape in shapes:
            if shape.hp <= 0:
                shapes.remove(shape)
                player.money += shape.reward


    generate_level(load_level("1map.txt"))
    create_shapes_way(load_level("1map.txt"))
    сreate_way_points(load_level("1map.txt"), 5)
    f2 = pygame.font.SysFont('comic sans', 66)

    def gameplay():
        draw_shapes_way()
        creating_tower()
        for points in way_points:
            pygame.draw.rect(first_level_screen, red, points)
        for tower in towers:
            tower.Draw()
            tower.shooting()
        for shape in shapes:
            shape.Move()
            shape.Draw()
        for bullet in bullets:
            homing = homing_calculation(bullet.x, bullet.y, shapes[0].x, shapes[0].y)
            bullet.move(homing[0], homing[1])
            if homing[2] <= bullet.speed:
                shapes[0].hp -= bullet.dmg
                bullets.remove(bullet)
            bullet.Draw()
        if_shape_died()

    enemys_in_map = False # есть ли враги на карте


    while True:
        if main_menu_flag:
            load_main_menu()  # Функция загрузки главного меню
        if level_choise_flag:
            load_level_choise_menu()  # Функция загрузки меню выбора уровней
        if first_lvl_start:
            if enemys_in_map == False:
                creating_enemys()
                enemys_in_map = True
            load_first_level()

            money = f2.render(str(player.money), False, yellow)
            health = f2.render(str(player.health), False, red)

            money_text = f2.render(("Монеты:"), False, yellow)
            health_text = f2.render(("Жизни:"), False, red)
            first_level_screen.blit(money, (1300, 20))
            first_level_screen.blit(health, (700, 20))
            first_level_screen.blit(money_text, (1020, 20))
            first_level_screen.blit(health_text, (470, 20))
            gameplay()
        print(clock.get_fps())

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
                if first_lvl_start:
                    x, y = pygame.mouse.get_pos()
                    for i in range(0, 27):  # всего 26 клеточек на 1 карте
                        if towers_group.sprites()[i].rect.collidepoint(x, y):
                            print(i)  # печатает номер выбранной клеточки
                            secret_important_number = i  # запоминает выбранную клеточку
        pygame.display.update()
        clock.tick(FPS)
pygame.quit()
