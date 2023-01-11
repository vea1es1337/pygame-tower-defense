# В этом файле хранятся все классы, использующиеся в программе


import pygame
import os
import sys
import math

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class ButtonBackLvlChoise(pygame.sprite.Sprite):  # Класс спрайта кнопки "назад" в меню выбора уровня
    image = load_image("level_choise_back_btn.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonBackLvlChoise.image
        self.rect = self.image.get_rect()
        self.rect.x = 1126
        self.rect.y = 50

    def change_rect(self, x, y):
        self.rect.x = x
        self.rect.y = y


class ButtonFirstLvl(pygame.sprite.Sprite):  # Класс спрайта кнопки выбора первого уровня
    image = load_image("first_lvl_button.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonFirstLvl.image
        self.rect = self.image.get_rect()
        self.rect.x = 95
        self.rect.y = 380

    def change_rect(self, x, y):
        self.rect.x = x
        self.rect.y = y


class ButtonMainMenu(pygame.sprite.Sprite):
    image = load_image("button.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ButtonMainMenu.image


class LevelChoiseMenuButton(pygame.sprite.Sprite):
    image = load_image("level_choise_button.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = LevelChoiseMenuButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def change_rect(self, x, y):  # Смена положения спрайта
        self.rect.x = x
        self.rect.y = y


class ShopButton(pygame.sprite.Sprite):
    image = load_image("shop_button.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ShopButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def change_rect(self, x, y):  # Смена положения спрайта
        self.rect.x = x
        self.rect.y = y


class FirstTower(pygame.sprite.Sprite):
    image = load_image("common_lvl1.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = FirstTower.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    def change_rect(self, x, y):
        self.rect.x = x
        self.rect.y = y


class ExitButton(pygame.sprite.Sprite):
    image = load_image("quit_button.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = ExitButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10


    def change_rect(self, x, y):  # Смена положения спрайта
        self.rect.x = x
        self.rect.y = y

class SelectUpgradeMenu(pygame.sprite.Sprite):  # класс спрайта менюшки выбора башни
    image = load_image("tower_select.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = SelectUpgradeMenu.image
        self.rect = self.image.get_rect()
        self.rect.x = 1500
        self.rect.y = 100

    def change_rect(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Tower:
    def __init__(self, x, y, damage, fire_rate, price, radius):
        self.x = x
        self.y = y
        self.damage = damage
        self.fire_rate = fire_rate
        self.fire_rate_tick = 0
        self.price = price
        self.radius = radius

    def Draw(self, window):
        pygame.draw.circle(window, [self.x, self.y])



class Player:
    def __init__(self, Money, Health):
        self.money = Money
        self.health = Health
class TowerCell(pygame.sprite.Sprite):
    image = load_image("cell1.png")
    tile_width = tile_height = 128
    def __init__(self, pos_x, pos_y, *group):
        super().__init__(*group)
        self.image = TowerCell.image
        self.rect = self.image.get_rect().move(
            TowerCell.tile_width * pos_x, TowerCell.tile_height * pos_y)