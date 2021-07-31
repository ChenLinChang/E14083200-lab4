import pygame
import os
import math
from enemy import Enemy

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """
        x1, y1 = enemy.get_pos() #x1,y1儲存enemy的位置
        distance_enemy_tower = math.sqrt((x1 - self.center[0]) ** 2 + (y1 - self.center[1]) ** 2) #計算enemy和tower的距離
        if distance_enemy_tower<=self.radius: #若距離在攻擊範圍內,回傳true,否則回傳false
            return 1
        else:
            return 0


    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        transparent_surface = pygame.Surface(win.get_size(), pygame.SRCALPHA) #製作畫布
        transparency = 80 # define transparency: 0~255, 0 is fully transparent
        # draw the rectangle on the transparent surface
        pygame.draw.circle(transparent_surface, (192,192,192, transparency), self.center,self.radius,0) #畫布上作透明圓形
        win.blit(transparent_surface,(0,0))



class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = True  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """

        #判定是否達到冷卻時間,達到即歸零
        if self.cd_count<self.cd_max_count:
            self.cd_count+=1
            return 0
        else:
            self.cd_count=0
            return 1






    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """

        for atk in enemy_group.get():
            if self.is_cool_down() and self.range_circle.collide(atk): #判定tower是否冷卻及enemy是否在範圍內
                atk.get_hurt(self.damage) #對enemy造成傷害
                break







    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        #回傳游標是否在矩形範圍內的布林值
        if x>=self.rect.centerx-self.rect.width/2 and x<=self.rect.centerx+self.rect.width/2 and y>=self.rect.centery-self.rect.height/2 and y<=self.rect.centery+self.rect.height/2:
        #if (x,y)<=(self.rect.x,self.rect.y) and (x,y) <= self.rect.bottomright:
            return True
        else:
            return False



    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

