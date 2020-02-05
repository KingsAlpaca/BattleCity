# Battle City Remake
# by Qianzhou Wang

# import the library needed, which are 'pygame', 'sys' and 'random'
import pygame
import sys
import random

# 'pygame.locals' will allow me to use some variables such as a key on the keyboard directly
from pygame.locals import *

# Point class
# Vector which has two parameter can be treated as a point have x, y coordinate.
# Such as position, velocity etc.
class Point(object):

    # initialize Point class
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # X property
    def getx(self): return self.__x

    def setx(self, x): self.__x = x
    x = property(getx, setx)

    # Y property
    def gety(self): return self.__y

    def sety(self, y): self.__y = y
    y = property(gety, sety)


# Sprite is widely used in game design. Anything appearing in the game can be a sprite.
# For example, tanks in the Battle City are sprites. In this case, there are two different
# sprite classes. The DynamicSprite is for those sprites having dynamic images.
# The tracks of the tank move, therefore, tank is a DynamicSprite.
# DynamicSprite class is an extension of the pygame.sprite.Sprite class
class DynamicSprite(pygame.sprite.Sprite):

    # initialize DynamicSprite class
    def __init__(self):

        # extend the base Sprite class
        pygame.sprite.Sprite.__init__(self)

        # master_image is the sprite sheet making up with the images for lots of sprites
        self.master_image = None
        self.rect = None
        self.image = None

        # to allow the sprite to have dynamic images, the class will record the frame numbers.
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 1
        self.last_frame = 1

        # columns is the number of columns on the master image or sprite sheet, which allow the program to calculate
        # the sub-image position automatically
        self.columns = 1

        # time is also recorded to control the fps
        self.last_time = 0

    # X property, where X is the x-coordinate of the sprite position on the screen
    def _getx(self): return self.rect.x

    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    # Y property, where Y is the y-coordinate of the sprite position on the screen
    def _gety(self): return self.rect.y

    def _sety(self, value): self.rect.y = value
    Y = property(_gety, _sety)

    # position property, where position is a combination of x and y
    def _getpos(self): return self.rect.topleft

    def _setpos(self, pos): self.rect.topleft = pos
    position = property(_getpos, _setpos)

    # function to load the image for the sprite
    def load(self, filename, width, height, columns):

        # load a image file as master_image
        self.master_image = pygame.image.load(filename).convert_alpha()

        # get_size return the size of the image
        m_width, m_height = self.master_image.get_size()

        # the whole game is running with a scale factor 3. For example, a brick wall has a 16x16 image.
        # But it appears as a 48x48 square on the screen
        self.master_image = pygame.transform.scale(self.master_image, (m_width*3, m_height*3))

        # set up frame size
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns

    def update(self, current_time, rate=30):

        # update animation frame number
        if current_time > self.last_time + rate:

            # automatically refresh the frame
            self.frame += 1

            # return to first frame when the frame number is too large
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        # build current frame only if it changed
        if self.frame != self.old_frame:

            # calculate the position of the next frame
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height

            # cut the subsurface out of the sprite sheet
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame


# StaticSprite is a class for those sprites which have a static image.
# For example, trees, bricks and walls etc. in the Battle City.
class StaticSprite(pygame.sprite.Sprite):

    # initialize StaticSprite class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.master_image = None
        self.rect = None
        self.image = None

    # X property
    def _getx(self): return self.rect.x

    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    # Y property
    def _gety(self): return self.rect.y

    def _sety(self, value): self.rect.y = value
    Y = property(_gety, _sety)

    # position property
    def _getpos(self): return self.rect.topleft

    def _setpos(self, pos): self.rect.topleft = pos
    position = property(_getpos, _setpos)

    # load up the image for the sprite from a file
    def load(self, filename, width, height, topleft_x, topleft_y):

        # load the master image from sprite sheet file
        self.master_image = pygame.image.load(filename).convert_alpha()
        m_width, m_height = self.master_image.get_size()

        # resize the master image to fix the screen with a scale factor of 3
        self.master_image = pygame.transform.scale(self.master_image, (m_width*3, m_height*3))

        # calculate the subsurface size and position
        self.rect = Rect(0, 0, width, height)
        rect = Rect(topleft_x, topleft_y, width, height)

        # cut out the useful area on the master_image
        self.image = self.master_image.subsurface(rect)


# classes to define environment objects
class Water(DynamicSprite):

    # initialize Water object
    def __init__(self):
        DynamicSprite.__init__(self)

        # load the image for the for the water object
        self.load("images/environment.png", 48, 48, 5)

        # set up the start frame and the end frame to allow DynamicSprite update the water object
        self.first_frame = 0
        self.last_frame = 1


class Bricks(StaticSprite):

    # initialize Brick object
    def __init__(self, brick_ground_type):
        StaticSprite.__init__(self)

        # load the image for 2 different types of bricks
        if brick_ground_type == 0:
            self.load("images/environment.png", 12, 12, 0, 48)
        if brick_ground_type == 1:
            self.load("images/environment.png", 12, 12, 12, 48)


# same with above
class Wall(StaticSprite):
    def __init__(self):
        StaticSprite.__init__(self)
        self.load("images/environment.png", 24, 24, 48, 48)


class Trees(StaticSprite):
    def __init__(self):
        StaticSprite.__init__(self)
        self.load("images/environment.png", 48, 48, 144, 0)


class Ice(StaticSprite):
    def __init__(self):
        StaticSprite.__init__(self)
        self.load("images/environment.png", 48, 48, 192, 0)


class Eagle(StaticSprite):
    def __init__(self):
        StaticSprite.__init__(self)
        self.load("images/environment.png", 48, 48, 144, 48)


# classes to define Enemy tanks objects
class BasicTank(DynamicSprite):

    # initialize BasicTank object
    def __init__(self, award=False):
        DynamicSprite.__init__(self)

        # number is used to identify player and enemy
        # player is one of 1-7, enemy is 8
        self.number = 8

        # enemy type is used to identify different types of enemies
        # it also help the DynamicSprite class to locate the frame for enemies
        self.enemy_type = 0

        # set the initial frame for a basic tank
        self.frame = 64

        # award BasicTank is another type of basic tank which has the same moving property, but uses another
        # group of frame images
        if award:
            self.enemy_type = 1

        # no initial velocity for an enemy
        self.velocity = Point(0.0, 0.0)

        # BasicTank moves at a speed of 3
        self.speed = 3

        # BasicTank fires bullets at a speed of 12
        self.bullet_speed = 12

        # BasicTank has a direction
        self.direction = 0

        # last fire time is used to time and control the gap between two launching
        self.last_fire_time = 0

        # ready to move is used to prevent tanks from moving to some places which aren't designed to reach
        self.ready_to_move = False

        # bullet on map allows tank to fire one bullet at a time
        self.bullet_on_map = 0

        # bullet time passed is used to prevent tanks from shooting too frequently
        self.bullet_time_passed = True

        # last move time is used to prevent tanks from turning for too many times when hit the boundary
        self.last_move_time = 0


# see above
class FastTank(DynamicSprite):
    def __init__(self, award=False):
        DynamicSprite.__init__(self)
        self.number = 8
        self.enemy_type = 2
        self.frame = 80
        if award:
            self.enemy_type = 3
        self.velocity = Point(0.0, 0.0)
        self.speed = 5
        self.bullet_speed = 12
        self.direction = 0
        self.last_fire_time = 0
        self.ready_to_move = False
        self.bullet_on_map = 0
        self.bullet_time_passed = True
        self.last_move_time = 0


class PowerTank(DynamicSprite):
    def __init__(self, award=False):
        DynamicSprite.__init__(self)
        self.number = 8
        self.enemy_type = 4
        self.frame = 96
        if award:
            self.enemy_type = 5
        self.velocity = Point(0.0, 0.0)
        self.speed = 4
        self.bullet_speed = 24
        self.direction = 0
        self.last_fire_time = 0
        self.ready_to_move = False
        self.bullet_on_map = 0
        self.bullet_time_passed = True
        self.last_move_time = 0


# ArmorTank is special type of tank which is flashing all time
# it has a specially designed update function which is different with the one used for DynamicSprite
class ArmorTank(pygame.sprite.Sprite):

    # the initialization of ArmorTank is an combination of DynamicSprites and Tanks
    def __init__(self, award=False):
        pygame.sprite.Sprite.__init__(self)
        self.number = 8
        self.enemy_type = 6
        self.frame = 112

        # life means ArmorTank needs to be shot for four times for an elimination
        self.life = 4
        self.last_life = 4

        if award:
            self.enemy_type = 7
        self.velocity = Point(0.0, 0.0)
        self.speed = 4
        self.bullet_speed = 12
        self.direction = 0
        self.last_fire_time = 0

        # hit by is recorded for the award
        self.hit_by = []

        self.ready_to_move = False
        self.bullet_on_map = 0
        self.bullet_time_passed = True

        self.master_image = None
        self.rect = None
        self.image = None

        # to allow the sprite to have dynamic images, the class will record the frame numbers.
        self.frame = 112
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 1
        self.last_frame = 1
        self.columns = 1

        # time is also recorded to control the fps
        self.last_update_time = 0
        self.last_flash_time = 0
        self.last_move_time = 0

    # X property, where X is the x-coordinate of the sprite position on the screen
    def _getx(self): return self.rect.x

    def _setx(self, value): self.rect.x = value
    X = property(_getx, _setx)

    # Y property, where Y is the y-coordinate of the sprite position on the screen
    def _gety(self): return self.rect.y

    def _sety(self, value): self.rect.y = value
    Y = property(_gety, _sety)

    # position property
    def _getpos(self): return self.rect.topleft

    def _setpos(self, pos): self.rect.topleft = pos
    position = property(_getpos, _setpos)

    # same with the load function for DynamicSprite
    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        m_width, m_height = self.master_image.get_size()
        self.master_image = pygame.transform.scale(self.master_image, (m_width*3, m_height*3))
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    # update function includes two different part
    # update loads the image of next frame(+1) for the tank
    # flash locates the frame by using a dictionary
    def update(self, current_time, update_rate=30, flash_rate=10):

        # update animation frame number
        if current_time > self.last_update_time + update_rate:

            # automatically refresh the frame
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_update_time = current_time

        # if the life remained has changed, frame of the ArmorTank also need to be changed
        if current_time > self.last_flash_time + flash_rate:
            if self.life != self.last_life:
                if self.life == 3:
                    self.frame = 136
                elif self.life == 2:
                    self.frame = 136
                elif self.life == 1:
                    self.frame = 112
                self.last_life = self.life

            # reference dictionary is used to find the next frame in a flash
            ref_dict = None
            if self.life == 4 and self.enemy_type == 7:
                ref_dict = {112: 120, 113: 121, 114: 122, 115: 123,
                            116: 124, 117: 125, 118: 126, 119: 127,
                            120: 112, 121: 113, 122: 114, 123: 115,
                            124: 116, 125: 117, 126: 118, 127: 119}
            elif self.life == 4 and self.enemy_type == 6:
                ref_dict = {112: 128, 113: 129, 114: 130, 115: 131,
                            116: 132, 117: 133, 118: 134, 119: 135,
                            128: 112, 129: 113, 130: 114, 131: 115,
                            132: 116, 133: 117, 134: 118, 135: 119}
            elif self.life == 3:
                ref_dict = {112: 136, 113: 137, 114: 138, 115: 139,
                            116: 140, 117: 141, 118: 142, 119: 143,
                            136: 112, 137: 113, 138: 114, 139: 115,
                            140: 116, 141: 117, 142: 118, 143: 119}
            elif self.life == 2:
                ref_dict = {128: 136, 129: 137, 130: 138, 131: 139,
                            132: 140, 133: 141, 134: 142, 135: 143,
                            136: 128, 137: 129, 138: 130, 139: 131,
                            140: 132, 141: 133, 142: 134, 143: 135}

            # when the ArmorTank has 1 life left, it doesn't flash any more
            if self.life == 1:
                pass
            else:
                self.frame = ref_dict[self.frame]

            self.last_flash_time = current_time

        # build current frame only if it changed
        # method is the same with above
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame


# classes to define the Power-Ups objects
class PowerUp(DynamicSprite):

    # initialize the PowerUps object
    def __init__(self):
        DynamicSprite.__init__(self)

        # the spawn time is recorded in order to kill the PowerUps object when time out
        self.spawn_time = ticks

    # kill the PowerUps object when time out
    def time_out(self, current_time):
        if current_time > self.spawn_time + 20000:
            self.kill()


class Grenade(PowerUp):

    # initialize the Grenade object
    def __init__(self):
        PowerUp.__init__(self)

        # set up the frame details for Grenade
        self.first_frame = 0
        self.last_frame = 1
        self.frame = 0

    # grenade function applies eliminations to all the enemies on a map
    def grenade(self, game_object):

        # kill the grenade image itself
        self.kill()

        # tell the game that no enemy left on the map
        game_object.enemy_on_map = 0

        # remove all the enemies from their group
        game_object.enemy_group.empty()
        enemy_list = game_object.enemy_list
        game_object.enemy_list = []

        # create explosions on the map
        for enemy in enemy_list:
            x, y = enemy.position
            x -= 24
            y -= 24

            explosion = Explosion("large")
            explosion.position = x, y
            game_object.explosion_group.add(explosion)

            # play the sound clip of an explosion
            play_sound("explosion")


# initialization is the same with above
class Helmet(PowerUp):
    def __init__(self):
        PowerUp.__init__(self)
        self.first_frame = 2
        self.last_frame = 3
        self.frame = 2

    # apply the effects of a helmet
    def helmet(self, game_object, tank_object):
        self.kill()

        # create a matchless sprite which is some patterns around the player
        game_object.matchless_sprite = Matchless()
        game_object.matchless_sprite.position = tank_object.position
        game_object.matchless_group.add(game_object.matchless_sprite)

        # enter the matchless mode
        tank_object.powerup_matchless = True

        # record the starting time of apply matchless in order to stop it later
        tank_object.last_powerup_matchless_time = ticks


class Shovel(PowerUp):
    def __init__(self):
        PowerUp.__init__(self)
        self.first_frame = 4
        self.last_frame = 5
        self.frame = 4

    # shovel function builds the base using steel instead of bricks
    def shovel(self, game_object):
        self.kill()

        # enter the shovel mode
        game_object.shoveled = True

        # remove all the remaining base
        for sprite in game_object.base_group.sprites():
            sprite.kill()

        # build the base using steel which is "wall" below
        game_object.base_builder("wall")

        # record the shoveling time in order to cancel the steel walls
        game_object.last_shovel_time = ticks


class Star(PowerUp):
    def __init__(self):
        PowerUp.__init__(self)
        self.first_frame = 6
        self.last_frame = 7
        self.frame = 6

    # function to improve the tier of player tank
    def star(self, tank_object, game_object):
        self.kill()

        # add one tier unless player is already of the highest
        if tank_object.number < 3:
            tank_object.number += 1

        # add one life is the player is of the highest tier
        else:
            game_object.player_life += 1

            # reload the life counter on the grey edge
            game_object.player_counter_loader()

        # improvement which should take place when the tier is increased
        if tank_object.number == 1:
            tank_object.bullet_speed = 24


class Tank(PowerUp):
    def __init__(self):
        PowerUp.__init__(self)
        self.first_frame = 8
        self.last_frame = 9
        self.frame = 8

    # function to apply the tank powerup
    def tank(self, game_object):
        self.kill()

        # add one life to the player
        game_object.player_life += 1
        game_object.player_counter_loader()


class Timer(PowerUp):
    def __init__(self):
        PowerUp.__init__(self)
        self.first_frame = 10
        self.last_frame = 11
        self.frame = 10

    # function to apply the timer powerup
    def timer(self, game_object):
        self.kill()

        # record the timer time in order to cancel the timer later
        game_object.last_timer_time = ticks

        # apply timer
        game_object.apply_timer = True


# objects on the right grey edge
class Counter(StaticSprite):

    # initialize Counter object
    def __init__(self, sprite_type="enemy"):
        StaticSprite.__init__(self)

        # there are two types of counter for enemies and players
        # load the images for the counters
        if sprite_type == "enemy":
            self.load("images/environment.png", 24, 24, 192, 144)

        elif sprite_type == "player":
            self.load("images/environment.png", 24, 24, 216, 144)


# same with above
class Flag(StaticSprite):
    def __init__(self):
        StaticSprite.__init__(self)
        self.load("images/environment.png", 48, 48, 192, 48)


class Number(StaticSprite):
    def __init__(self, num, num_color="black"):
        StaticSprite.__init__(self)

        # position of frame of the digit needs to be carefully calculated
        x = num % 5 * 24
        y = (num // 5 + 1) * 24

        # colors also affect the position of the subsurface
        if num_color == "yellow":
            y = (num // 5 + 7) * 24
        elif num_color == "white":
            y = (num // 5 + 9) * 24
        self.load("images/letters.png", 24, 24, x, y)


class PlayerName(StaticSprite):

    # initialization of another StaticSprite
    def __init__(self, name):
        StaticSprite.__init__(self)
        if name == 1:
            self.load("images/letters.png", 48, 24, 0, 72)

        elif name == 2:
            self.load("images/letters.png", 48, 24, 24, 72)


# objects may appear on the screen as texts
class GameOver(StaticSprite):
    def __init__(self):
        StaticSprite.__init__(self)
        self.load("images/letters.png", 96, 48, 0, 120)
        self.position = 312, 672


class PlayerTank(DynamicSprite):

    # initialize the PlayerTank object
    def __init__(self, num):
        DynamicSprite.__init__(self)

        # PlayerTank has a few similar qualities with EnemyTanks
        self.direction = 0
        self.velocity = Point(0.0, 0.0)
        self.speed = 5
        self.moving = False
        self.ready_to_move = False
        self.number = num
        self.bullet_on_map = 0

        # 123567 are the tiers of players which fire bullets of a higher speed
        if self.number in [1, 2, 3, 5, 6, 7]:
            self.bullet_speed = 24
        else:
            self.bullet_speed = 12

        # allow player to enter the matchless mode
        # there are two types of matchless, a short period of matchless after spawn and a long
        # period of matchless when the matchless power-up is applied
        self.spawn_matchless = False
        self.powerup_matchless = False
        self.last_spawn_matchless_time = 0
        self.last_powerup_matchless_time = 0


# Matchless object is the patterns around the player tank when it is matchless
class Matchless(DynamicSprite):
    def __init__(self):
        DynamicSprite.__init__(self)
        self.load("images/environment.png", 48, 48, 5)
        self.first_frame = 20
        self.last_frame = 21
        self.frame = 20


class Bullet(StaticSprite):

    # initialize Bullet object
    def __init__(self, direction, tank):
        StaticSprite.__init__(self)

        # bullet has a direction when it is fired
        self.direction = direction

        # each bullet belongs to a tank
        self.tank = tank

        # exist allow the function to detect its collision
        self.exist = True

        # different bullets may have different speed
        self.speed = tank.bullet_speed

        # ready to move prevent bullets from moving to places which are prohibited
        self.ready_to_move = True

        # last move time is recorded to prevent too many position updates
        self.last_move_time = 0

        # bullets with different launching directions has different images
        # a, b, c, d are width, height, x-coordinate of topleft and y-coordinate of topleft
        a, b, c, d = 0, 0, 0, 0
        if self.direction == 0:
            a, b, c, d = 9, 12, 0, 3
        elif self.direction == 1:
            a, b, c, d = 12, 9, 15, 6
        elif self.direction == 2:
            a, b, c, d = 9, 12, 30, 3
        elif self.direction == 3:
            a, b, c, d = 12, 9, 45, 6

        # load the image for the bullet sprite
        self.load("images/bullet.png", a, b, c, d)


class Explosion(DynamicSprite):

    # initialize explosion object
    def __init__(self, explosion_type):
        DynamicSprite.__init__(self)

        # explosions has a sequence of images
        self.load("images/explosions.png", 96, 96, 5)
        self.first_frame = 0
        self.last_frame = 4
        self.frame = 0

        # Explosion has a frame size of 96 * 96 pixel
        rect = Rect(0, 0, 96, 96)

        # get the subsurface for the explosion master image
        self.image = self.master_image.subsurface(rect)
        self.explosion_type = explosion_type

    # explode function changes the frame of the Explosion object to form an explosion
    def explode(self, current_time, rate=120):
        kill_frame = 0

        # small explosion only uses the first 3 frames of the sequence
        if self.explosion_type == "small":
            kill_frame = 2

        # large explosion uses all the 5 frame of the sequence
        elif self.explosion_type == "large":
            kill_frame = 4

        # update the frame when certain time has past
        if current_time > self.last_time + rate:
            self.last_time = current_time
            self.frame += 1

            # calculate the coordinates of the subsurface
            x = 96 * self.frame
            y = 0
            rect = Rect(x, y, 96, 96)

            # update the image
            self.image = self.master_image.subsurface(rect)

            # when the frame number is greater than the kill frame number, kill the object
            if self.frame == kill_frame:
                self.kill()


# Menu object is the background image of the starting menu
class MenuImage(StaticSprite):
    def __init__(self):
        StaticSprite.__init__(self)
        self.load("images/menu.png", 768, 672, 0, 0)
        self.position = 0, 672


# function to calculate the velocity depending on directions
# direction are recorded in even numbers which also represent the frame position of each direction
def calc_velocity(direction, vel):
    velocity = Point(0, 0)
    if direction == 0:  # north
        velocity.y = -vel
    elif direction == 2:  # west
        velocity.x = -vel
    elif direction == 4:  # south
        velocity.y = vel
    elif direction == 6:  # east
        velocity.x = vel
    return velocity


# function to reverse the direction of moving objects, especially for enemy tanks
def reverse_direction(sprite):
    if sprite.direction == 0 or sprite.direction == 2:
        sprite.direction += 4
    elif sprite.direction == 4 or sprite.direction == 6:
        sprite.direction -= 4


# turning adjustment function is a function to help the player to make a turn
# when the position of the player is a few pixel off from the gap, this function helps to place the player in between
# the gap. The trigger of the function is when a key of turning is pressed
def turning_adjustment(sprite):

    # get the position of the player
    x, y = sprite.position

    # find the nearest allowed position
    reminder_x = x % 24
    reminder_y = y % 24

    # all the turnings have been adjusted, which means the player is always on a special line
    # when the tank is moving from vertical line to horizontal line, change the y coordinate to the nearest
    # allowed horizontal line
    if reminder_x == 0:
        if reminder_y < 12:
            sprite.position = x, y - reminder_y
        elif reminder_y >= 12:
            sprite.position = x, y + (24 - reminder_y)

    # when moving from horizontal line to vertival line
    elif reminder_y == 0:
        if reminder_x < 12:
            sprite.position = x - reminder_x, y
        elif reminder_x >= 12:
            sprite.position = x + (24-reminder_x), y


# function to turn right
def turn_right(sprite):
    sprite.direction -= 2
    if sprite.direction == -2:
        sprite.direction = 6


# function to turn left
def turn_left(sprite):
    sprite.direction += 2
    if sprite.direction == 8:
        sprite.direction = 0


# transform the position of the top left corner of tank image to the position of the top left corner of bullet image
# the position of the top left corner of tank is named as x and y
# transformation varies when tank is moving towards different directions
def fire_position(x, y, direction):
    if direction == 0:
        x += 18
        y -= 12
    elif direction == 1:
        x -= 12
        y += 21
    elif direction == 2:
        x += 18
        y += 48
    elif direction == 3:
        x += 48
        y += 21
    # the position of the top left corner of bullet if return
    return x, y


# function to play the audio clip
def play_sound(sound):

    # combine the name str to make a file name
    file_name = "sounds/" + sound + ".ogg"

    # load the sound from a file
    audio_clip = pygame.mixer.Sound(file_name)

    # find an empty channel to play the sound
    # "True" force the program to find a channel, which can be the least using channel
    channel = pygame.mixer.find_channel(True)

    # play the sound clip
    channel.play(audio_clip)


# print the numbers with the original font on the screen
def print_number(num, num_color, topright_x, y, group):

    # length of the number is calculated as each digit is a individual sprite
    length = len(str(num))
    for i in range(length):

        # get the digit by modding 10
        digit = num % 10

        # remove the digit which has been recorded
        num //= 10

        # calculate the x coordinate for the digit based on the x coordinate of the last digit of the whole number
        x = topright_x - 24 * (i + 1)

        # create a number sprite
        number = Number(digit, num_color)

        # place the sprite on the map
        number.position = x, y
        group.add(number)


# The whole Battle City has been modified as four parts: Stating Menu, Level Menu,
# Game of a Level and Scoring Board
# Game object forms a whole game of a level staring from loading the map,
# ending with the success of failure of the player
class Game(object):
    # initialize Game class
    def __init__(self, pygame_screen, game_level):
        global player_1, life

        # get the screen for the game
        self.screen = pygame_screen

        # load the number of the level from input from outside
        self.level = game_level

        # enemy spawn list records the order of spawing enemies
        self.enemy_spawn_list = []

        # counter list includes the enemy counter on the grey edge
        self.counter_list = []

        # enemy list includes the enemies on the map
        self.enemy_list = []

        # player tank is the tank sprite controlled by the player
        # as the tier need to be inherited from the previous level, player tank is defined from outside
        self.player_tank = player_1

        # matchless sprite is the pattern around the player when the player is matchless
        self.matchless_sprite = None

        # player life record the remaining life of the player
        self.player_life = life

        # game over is a status of the game
        self.game_over = False

        # game over time is also recorded in order to end the game at a certain time later
        self.game_over_time = 0

        # game success is a status of the game
        self.success = False

        # last elimination time is recorded to prevent enemies from spawning at an unexpected rate
        self.last_elimination_time = None

        # last player elimination time is recorded in order to re-spawn the player at a certain time later
        self.last_player_elimination_time = None

        # last spawn time is also used to control the spawning rate of enemies
        self.last_spawn_time = None

        # enemy on map doesn't allow more than for enemies on the map
        self.enemy_on_map = 0

        # elimination all is used to control the end of the game
        self.elimination_all = False
        self.elimination_all_time = 0

        # last shovel time is used to end the shovel at a certain time
        self.last_shovel_time = 0

        # shoveled is a status of the game
        self.shoveled = False

        # same apply to timer as shovel
        self.last_timer_time = 0
        self.apply_timer = False

        # counters recording the numbers of eliminations in order to show them on the scoring board
        self.eliminate_basic = 0
        self.eliminate_fast = 0
        self.eliminate_power = 0
        self.eliminate_armor = 0

        # score also needs to be counted
        self.score = 0

        # before the start of the game, set the game mode to initialize to load the map etc. as a few objects
        # don't need to be loaded again during the play
        self.initialize = True

        # create pygame sprite groups to allow group updates and paintings
        self.bricks_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.trees_group = pygame.sprite.Group()
        self.ice_group = pygame.sprite.Group()
        self.base_group = pygame.sprite.Group()
        self.eagle_group = pygame.sprite.Group()
        self.counter_group = pygame.sprite.Group()
        self.flag_group = pygame.sprite.Group()
        self.player_counter_group = pygame.sprite.Group()
        self.game_over_text_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.matchless_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.armor_tank_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

    # function to load the map for a level
    def map_loader(self):
        # combine a few strings to make up the filename of the level map file
        filename = "levels/" + str(self.level) + ".txt"

        # open file
        file = open(filename)

        # read the file and record the environment types using list in python
        environment_list = []
        for line in file:
            line = line[0:-1]
            line_list = line.split(" ")
            environment_list.append(line_list)

        # get the type in row-column order
        for i in range(13):
            for j in range(13):
                ground_type = environment_list[i][j]

                # calculate the position of the top right corner of a environment unit square
                # 48 and 24 are used to fit the grey edges
                basic_x, basic_y = 48 * j + 48, 48 * i + 24

                # ground type "00" means nothing in the unit square
                if ground_type == "00":
                    pass

                # "01" to "05" are the bricks filled with different part
                # "01" is half brick on the right, "02" is half brick on the bottom
                # "03" is half brick on the left, "04" is half brick on the top
                # "05" is a full brick
                elif ground_type == "01" or ground_type == "02" or ground_type == "03" \
                        or ground_type == "04" or ground_type == "05":

                    # x and y are the adjustment amount specially for bricks
                    x_list = [0]
                    y_list = [0]

                    # each full brick is made up of 16 small bricks in a 4x4 matrix
                    # 2, 3 in x list means the 3rd and 4th columns are filled
                    # 1, 2, 3, 4 in y list means the 1st, 2nd, 3rd and 4th rows are filled
                    if ground_type == "01":
                        x_list = [2, 3]
                        y_list = [0, 1, 2, 3]

                    # same apply as above
                    elif ground_type == "02":
                        x_list = [0, 1, 2, 3]
                        y_list = [2, 3]
                    elif ground_type == "03":
                        x_list = [0, 1]
                        y_list = [0, 1, 2, 3]
                    elif ground_type == "04":
                        x_list = [0, 1, 2, 3]
                        y_list = [0, 1]
                    elif ground_type == "05":
                        x_list = [0, 1, 2, 3]
                        y_list = [0, 1, 2, 3]

                    # small bricks have two different type
                    # calculate the type of the small bricks
                    for x in x_list:
                        for y in y_list:
                            if (x + y) % 2 == 0:
                                # create a type 0 small brick
                                bricks = Bricks(0)
                            if (x + y) % 2 == 1:
                                # create a type 1 small brick
                                bricks = Bricks(1)

                            # place the small brick in the right position
                            bricks.position = basic_x + 12 * x, basic_y + 12 * y

                            # add the brick to the bricks group
                            self.bricks_group.add(bricks)

                # "06" to "10" are the wall filled with different part
                # "06" is half wall on the right, "07" is half wall on the bottom
                # "08" is half wall on the left, "09" is half wall on the top
                # "10" is a full wall
                elif ground_type == "06" or ground_type == "07" or ground_type == "08" \
                        or ground_type == "09" or ground_type == "10":

                    # a full wall is made up of four pieces of steel
                    if ground_type == "10":

                        # loop through the adjustment quantities
                        for x in [0, 24]:
                            for y in [0, 24]:

                                # create a small piece of steel
                                wall = Wall()

                                # place the steel at the right position
                                wall.position = basic_x + x, basic_y + y

                                # add the steel into the wall group
                                self.wall_group.add(wall)

                    # otherwise, walls are made up of two pieces of steel
                    else:
                        wall1 = Wall()
                        wall2 = Wall()

                        # apply the position adjustment for each situation
                        # place the steel
                        if ground_type == "06":
                            wall1.position = basic_x + 24, basic_y
                            wall2.position = basic_x + 24, basic_y + 24
                        elif ground_type == "07":
                            wall1.position = basic_x, basic_y + 24
                            wall2.position = basic_x + 24, basic_y + 24
                        elif ground_type == "08":
                            wall1.position = basic_x, basic_y
                            wall2.position = basic_x, basic_y + 24
                        elif ground_type == "09":
                            wall1.position = basic_x, basic_y
                            wall2.position = basic_x + 24, basic_y

                        # add the steel to the wall group
                        self.wall_group.add(wall1)
                        self.wall_group.add(wall2)

                # create a water sprite when type is "11"
                elif ground_type == '11':
                    water = Water()

                    # place the water sprite
                    water.position = basic_x, basic_y

                    # add water sprite to the water group
                    self.water_group.add(water)

                # same as above
                elif ground_type == "12":
                    trees = Trees()
                    trees.position = basic_x, basic_y
                    self.trees_group.add(trees)

                elif ground_type == "13":
                    ice = Ice()
                    ice.position = basic_x, basic_y
                    self.ice_group.add(ice)

    # function to build the base
    def base_builder(self, base_type):

        # clear the existing sprites in the base group before building the base
        self.base_group.empty()

        # when building a wall
        if base_type == "wall":

            # hard code the position of each piece of steel in a list
            position_list = [[264, 552], [264, 576], [264, 600], [288, 552], [312, 552], [336, 552], [336, 576],
                             [336, 600]]

            # create the steel sprite and place them in the right position
            for i in range(8):
                wall = Wall()

                # 48 and 24 are used to fit the grey edges
                wall.position = position_list[i][0] + 48, position_list[i][1] + 24

                # add steel into both base group and wall group in order to manage them easily
                self.base_group.add(wall)
                self.wall_group.add(wall)

        # when building base using bricks
        if base_type == "bricks":

            # hard code the position of two different types of small bricks into lists
            position_zero_list = [[264, 552], [264, 576], [264, 600], [276, 564], [276, 588], [276, 612], [288, 552],
                                  [300, 564], [312, 552], [324, 564], [336, 552], [336, 576], [336, 600], [348, 564],
                                  [348, 588], [348, 612]]
            position_one_list = [[264, 564], [264, 588], [264, 612], [276, 552], [276, 576], [276, 600], [288, 564],
                                 [300, 552], [312, 564], [324, 552], [336, 564], [336, 588], [336, 612], [348, 552],
                                 [348, 576], [348, 600]]

            # create the sprite and place them into right positions as above
            for i in range(16):
                bricks0 = Bricks(0)
                bricks1 = Bricks(1)
                bricks0.position = position_zero_list[i][0] + 48, position_zero_list[i][1] + 24
                bricks1.position = position_one_list[i][0] + 48, position_one_list[i][1] + 24
                self.base_group.add(bricks0)
                self.bricks_group.add(bricks0)
                self.base_group.add(bricks1)
                self.bricks_group.add(bricks1)

    # function to load the eagle symbol on the map
    def eagle_builder(self):

        # create the eagle sprite
        eagle = Eagle()

        # 48 and 24 are used to fit the grey edges
        eagle.position = 288 + 48, 576 + 24

        # add the eagle sprite to the eagle group
        self.eagle_group.add(eagle)

    # load the flag on the grey edge
    def flag_loader(self):

        # create, place and manage the flag sprite
        flag = Flag()
        flag.position = 696, 528
        self.flag_group.add(flag)

        # number of the level is also shown on the screen
        # calculate the digits and create responding number sprite
        num_2 = self.level % 10
        number_2 = Number(num_2)
        number_2.position = 720, 576
        self.flag_group.add(number_2)

        # number of level may be a single digit
        # in this case, don't need to create a second number
        num_1 = self.level // 10
        if num_1 != 0:
            number_1 = Number(num_1)
            number_1.position = 696, 576
            self.flag_group.add(number_1)

    # load the player life counter on the grey edge
    def player_counter_loader(self):

        # create the counter only if the player is still alive (having more than 0 life left)
        if self.player_life > -1:
            self.player_counter_group.empty()

        # counter is a image
        # load, place and manage the player counter
        counter = Counter("player")
        counter.position = 696, 384
        self.player_counter_group.add(counter)

        # create a number sprite to show the remaining life of the player
        num = self.player_life
        number = Number(num)
        number.position = 720, 384
        self.player_counter_group.add(number)

        # player name is also created in order to identify the player when there is a second player
        player_name = PlayerName(1)
        player_name.position = 696, 360
        self.player_counter_group.add(player_name)

    # load the counters on the grey edge
    def enemy_counter_loader(self):

        # load all of the 20 counters initially
        for i in range(20):

            # create a enemy counter sprite
            counter = Counter()

            # calculate the position based on the order of counters themselves
            x = 720
            if i % 2 == 0:
                x = 696
            y = 48 + (i // 2) * 24

            # place the counter and add them to group and list in order to manage
            counter.position = x, y
            self.counter_group.add(counter)
            self.counter_list.append(counter)

    # load a list of the spawning order of enemy tanks
    def enemy_spawn_list_loader(self):

        # spawn order is hard coded as a string
        # the last digit of the string is the first one to be created
        # as it is easy to remove the last element of a list
        level_dict = {1:  "22000000000000000000", 2:  "00000000000000222266",
                      3:  "66222200000000000000", 4:  "66600222224444444444",
                      5:  "22222000000006644444", 6:  "66000000000224444444",
                      7:  "00000004444442222000", 8:  "00000002222664444444",
                      9:  "66644444442222000000", 10: "66444422000000000000",
                      11: "22222444466666622222", 12: "66666622222244444444",
                      13: "66662222222244444444", 14: "66666622224444444444",
                      15: "66666666222222222200", 16: "66220000000000000000",
                      17: "00000000666666662266", 18: "22222222444444006666",
                      19: "44440000666666662222", 20: "66666666440022222222",
                      21: "66660000002244444444", 22: "66664400000022222222",
                      23: "22222222224444666666", 24: "00000000002222664444",
                      25: "66666666662222222244", 26: "44440000666666222222",
                      27: "00222222226666666644", 28: "44000000000000000622",
                      29: "66666622224444444444", 30: "66664444222222220000",
                      31: "44466666622222222444", 32: "22224400000066666666",
                      33: "22224444666666662222", 34: "66666622222222224444",
                      35: "66666666662222224444"}

        # find the enemy spawn list for a specific level using the dictionary above
        self.enemy_spawn_list = list(level_dict[self.level])

        # 3 random tanks in a level are award enemies
        # generate 3 random integers between 0 and 19 (no repeat)
        award_order_list = []
        while len(award_order_list) != 3:
            index_num = random.randint(0, 19)
            if index_num not in award_order_list:
                award_order_list.append(int(index_num))

        # apply the change to the chosen enemies
        for i in award_order_list:
            enemy_type = int(self.enemy_spawn_list[i])

            # type += 1 means change them to the award type but keep the properties
            enemy_type += 1
            self.enemy_spawn_list[i] = str(enemy_type)

    # load the player tank on the map
    def player_tank_loader(self, tank):

        # inherit the tank from outside
        self.player_tank = tank

        # load the sequence images for the tank
        self.player_tank.load("images/tanks.png", 48, 48, 8)

        # place the tank in the starting position and give it and upwards direction
        self.player_tank.position = 192 + 48, 576 + 24
        self.player_tank.direction = 0

        # add the tank to player group in order to manage
        self.player_group.add(self.player_tank)

        # create the matchless sprite at the same time as player is matchless for a while after spawn
        self.matchless_sprite = Matchless()

        # place and add the matchless sprite to group
        self.matchless_sprite.position = 192 + 48, 576 + 24
        self.matchless_group.add(self.matchless_sprite)

        # apply matchless and record the time
        self.player_tank.spawn_matchless = True
        self.player_tank.last_spawn_matchless_time = ticks

    # load a enemy tanks on the map
    def enemy_tank_loader(self, enemy_type, position):
        enemy = None

        # load a basic tank if type of enemy is 0
        if enemy_type == 0:
            enemy = BasicTank()

        # load a award basic tank is the type of enemy is 1
        elif enemy_type == 1:
            enemy = BasicTank(True)

        # same as above
        elif enemy_type == 2:
            enemy = FastTank()
        elif enemy_type == 3:
            enemy = FastTank(True)
        elif enemy_type == 4:
            enemy = PowerTank()
        elif enemy_type == 5:
            enemy = PowerTank(True)
        elif enemy_type == 6:
            enemy = ArmorTank()
        elif enemy_type == 7:
            enemy = ArmorTank(True)

        # load the dynamic sprite images sequence
        enemy.load("images/tanks.png", 48, 48, 8)

        # place the enemy in the right position and set them pointing downwards
        enemy.position = position
        enemy.direction = 4

        # add the enemy sprite to enemy group if it is not an armor tank
        if enemy_type in [0, 1, 2, 3, 4, 5]:
            self.enemy_group.add(enemy)

        # add the enemy sprite to armor tank group as it is managed by another way
        elif enemy_type in [6, 7]:
            self.armor_tank_group.add(enemy)

        # add the enemy to the enemy list in order to identify the enemies on the map
        self.enemy_list.append(enemy)
        self.enemy_on_map += 1

        # record the spawn time to prevent enemies from spawning at an unexpected rate
        self.last_spawn_time = ticks

    # control the loading process of enemy tanks
    def load_enemy(self):
        # only spawn enemy when there is enemy left for a level
        if self.enemy_spawn_list:

            # load the enemy only if it is a certain time after last elimination and spawn
            time_after_spawn = ticks - self.last_spawn_time
            time_after_elimination = ticks - self.last_elimination_time
            spawn = False

            # no more than 4 enemies are allowed on the map at the same time
            if self.enemy_on_map < 4:
                if time_after_spawn > 4000:

                    # for the first 4 enemies, there is no consideration on elimination gap
                    if len(self.enemy_spawn_list) > 15:
                        spawn = True

                    elif time_after_elimination > 1000:
                        spawn = True

            if spawn:

                # spawn position also follows a pattern
                reminder = len(self.enemy_spawn_list) % 3

                # calculate the spawn position based on the remainder of dividing 3
                position = 0 + 48, 0 + 24
                if reminder == 2:
                    position = 288 + 48, 0 + 24
                elif reminder == 1:
                    position = 576 + 48, 0 + 24

                # get the type of enemy that need to be created
                enemy_type = int(self.enemy_spawn_list[-1])

                # remove it from the spawn list
                self.enemy_spawn_list.pop()

                # load the enemy tank on the right position
                self.enemy_tank_loader(enemy_type, position)

                # remove 1 counter from the right grey edge as well as the list
                counter = self.counter_list[-1]
                self.counter_list.pop()
                if counter in self.counter_group:
                    self.counter_group.remove(counter)

    # function to move a tank
    def move_tank(self, tank):

        # test is a StaticSprite to test whether there is a empty space ahead
        test = StaticSprite()

        # test sprite has a area of 48x48 pixels
        test.load("images/environment.png", 48, 48, 0, 0)

        # calculate the position for the test sprite when the player is heading upwards
        # as tanks are only allow to fit into the gap with a depth of at least 24 pixels
        # positions need to be carefully calculated
        # more details on the document
        if tank.direction == 0:
            test.X = tank.X
            test.Y = (tank.Y - 24) // 24 * 24
            distance = tank.Y - test.Y - 24

        # same rules apply when the player is heading toward other directions
        elif tank.direction == 2:
            test.X = (tank.X - 24) // 24 * 24
            test.Y = tank.Y
            distance = tank.X - test.X - 24
        elif tank.direction == 4:
            test.X = tank.X
            reminder = tank.Y % 24
            if reminder == 0:
                test.Y = tank.Y + 24
            else:
                test.Y = tank.Y + 48 - reminder

            # distance is the value of the distance between the tank and the boundary
            distance = test.Y - tank.Y - 24
        elif tank.direction == 6:
            reminder = tank.X % 24
            if reminder == 0:
                test.X = tank.X + 24
            else:
                test.X = tank.X + 48 - reminder
            test.Y = tank.Y
            distance = test.X - tank.X - 24

        # place the test sprite
        test.position = test.X, test.Y

        # detect the collisions between test sprite and all the other prohibited sprites
        group_list = [self.bricks_group, self.wall_group, self.water_group, self.base_group, self.eagle_group]
        for group in group_list:

            # collision is a value to show whether collisions happens
            collision = pygame.sprite.spritecollideany(test, group)

            if collision:

                # if distance is still huge, larger than the minimum moving distance of a tank
                if distance > tank.speed:

                    # ignore the the gap
                    pass
                else:

                    # if the gap is smaller than the minimum moving distance, ignore the tanks' original speed
                    # and filling into the gap
                    tank.velocity = calc_velocity(tank.direction, distance)

                    # is the tank is right in front of the boundary, stop the movement
                    if distance == 0:
                        tank.ready_to_move = False
            else:
                pass

        # kill the test sprite
        test.kill()

    # function to move a player
    def move_player(self, player):

        # get the keyboard input from outside

        global keys, release

        # decide the movement of player 1
        # player sometimes becomes a none type based on a mystery
        # ignore if fails
        if type(player) != PlayerTank:
            return

        # set the ready to move to active
        player.ready_to_move = True

        # control of the player 1
        if player.number in [0, 1, 2, 3]:

            # fire a bullet is space is released
            if "SPACE" in release:

                # if the player is a tier 3 or 4 tank, 2 bullets are allowed on the map at the same time
                if player.number in [2, 3]:

                    # if the bullet fired by a player is less than 2
                    if player.bullet_on_map < 2:

                        # allow the launching and create the bullet sprite
                        direction = player.direction // 2
                        self.player_fire(player.X, player.Y, direction, player)

                        # play the sound of firing a bullet
                        play_sound("fire")

                # if the player is a tier 1 or 2 tank, only 1 bullet is allowed on the map at a time
                elif player.number in [0, 1]:

                    # only fire the bullet if no bullet fired by this player is on the map
                    if player.bullet_on_map == 0:
                        direction = player.direction // 2
                        self.player_fire(player.X, player.Y, direction, player)
                        play_sound("fire")

            # moving forward
            elif keys[K_w]:

                # when the player is heading horizontal direction
                # a turing adjustment to pull the player back to the vertical line is applied
                if player.direction == 2 or player.direction == 6:
                    turning_adjustment(player)

                # change the direction of the player to upwards, set the player to moving mode
                player.direction = 0
                player.moving = True

            # same rules apply for moving towards other directions
            # moving to the left
            elif keys[K_a]:
                if player.direction == 0 or player.direction == 4:
                    turning_adjustment(player)
                player.direction = 2
                player.moving = True

            # moving backward
            elif keys[K_s]:
                if player.direction == 2 or player.direction == 6:
                    turning_adjustment(player)
                player.direction = 4
                player.moving = True

            # moving to the right
            elif keys[K_d]:
                if player.direction == 0 or player.direction == 4:
                    turning_adjustment(player)
                player.direction = 6
                player.moving = True

            # if no key is pressed, set the player to static mode
            # this will stop the dynamic frame update for the player (see below)
            else:
                player.moving = False

        # movement of player 2, same rules as player 1
        elif player.number in [4, 5, 6, 7]:

            if keys[K_o]:
                if player.number in [6, 7]:
                    if player.bullet_on_map < 2:
                        direction = player.direction // 2
                        self.player_fire(player.X, player.Y, direction, player)
                        play_sound("fire")
                elif player.number in [4, 5]:
                    if player.bullet_on_map == 0:
                        direction = player.direction // 2
                        self.player_fire(player.X, player.Y, direction, player)
                        play_sound("fire")

            elif keys[K_UP]:
                if player.direction == 2 or player.direction == 6:
                    turning_adjustment(player)
                player.direction = 0
                player.moving = True

            elif keys[K_LEFT]:
                if player.direction == 0 or player.direction == 4:
                    turning_adjustment(player)
                player.direction = 2
                player.moving = True

            elif keys[K_DOWN]:
                if player.direction == 2 or player.direction == 6:
                    turning_adjustment(player)
                player.direction = 4
                player.moving = True

            elif keys[K_RIGHT]:
                if player.direction == 0 or player.direction == 4:
                    turning_adjustment(player)
                player.direction = 6
                player.moving = True

            else:
                player.moving = False

        # set animation frames based on player's direction
        # frame is based on the player number, player's direction and the tier of the player
        player.first_frame = player.direction + 8 * player.number
        player.last_frame = player.first_frame + 1

        # if the player's frame is below the first frame, simply set the first frame as the current frame
        if player.frame < player.first_frame:
            player.frame = player.first_frame

        #  when the player is not move, set it into the static mode
        if not player.moving:

            # stop animating when player is not pressing a key
            player.first_frame = player.last_frame = player.frame

        # otherwise, calculate the velocity as a point object for the player
        else:

            # move player in direction
            player.velocity = calc_velocity(player.direction, player.speed)

        # manually move the player
        if player.moving:

            # calculate the new position for the player
            x = player.X + player.velocity.x
            y = player.Y + player.velocity.y

            # if the player is going out onto the grey edge, stop it from moving
            if x < 0 + 48 or x > 576 + 48:
                player.ready_to_move = False
            if y < 0 + 24 or y > 576 + 24:
                player.ready_to_move = False

            # function defined above to check whether there are prohibit environment ahead
            self.move_tank(player)

            # when the player has completed and passed the full moving check list
            if player.ready_to_move:

                # apply the position change
                player.X += player.velocity.x
                player.Y += player.velocity.y

    # function to move an enemy tank
    # this is a very basic AI system for moving the enemies based on some random generated parameters
    # and the collisions between the enemies and the surroundings
    def move_enemy(self, enemy):

        if ticks > enemy.last_move_time + 30:
            enemy.ready_to_move = True
        else:
            enemy.ready_to_move = False

        enemy.velocity = calc_velocity(enemy.direction, enemy.speed)

        x = enemy.X + enemy.velocity.x
        y = enemy.Y + enemy.velocity.y
        if x < 0 + 48 or x > 576 + 48:
            enemy.ready_to_move = False
        if y < 0 + 24 or y > 576 + 24:
            enemy.ready_to_move = False

        self.move_tank(enemy)

        if enemy.ready_to_move:
            enemy.last_move_time = ticks
            enemy.X += enemy.velocity.x
            enemy.Y += enemy.velocity.y

        random_number = random.randint(0, 200)
        if random_number == 0 or not enemy.ready_to_move:
            random_direction = random.randint(0, 12)
            if random_direction < 6:
                turn_left(enemy)
            elif random_direction > 6:
                turn_right(enemy)
            else:
                reverse_direction(enemy)
            turning_adjustment(enemy)

        if ticks - enemy.last_fire_time < 1200:
            enemy.bullet_time_passed = False
        else:
            enemy.bullet_time_passed = True

        if enemy.bullet_on_map == 0 and enemy.bullet_time_passed:
            direction = enemy.direction // 2
            # create a bullet as a Bullet object
            bullet = Bullet(direction, enemy)
            # calculate the right position to fire the bullet
            bullet.position = fire_position(enemy.X, enemy.Y, direction)
            self.bullet_group.add(bullet)
            # continuously firing is not allowed
            enemy.bullet_on_map += 1
            enemy.last_fire_time = ticks
            self.bullet_collision(bullet, "immediate")

        if type(enemy) == ArmorTank:
            enemy.first_frame = enemy.direction + 8 * (enemy.frame // 8)
            enemy.last_frame = enemy.first_frame + 1
            if enemy.frame < enemy.first_frame:
                enemy.frame = enemy.first_frame

        else:
            enemy.first_frame = enemy.direction + 8 * (enemy.enemy_type + 8)
            enemy.last_frame = enemy.first_frame + 1
            if enemy.frame < enemy.first_frame:
                enemy.frame = enemy.first_frame

    # function to fire a bullet
    def player_fire(self, pos_x, pos_y, direction, player):

        # create a bullet as a Bullet object
        bullet = Bullet(direction, player)

        # calculate the right position to fire the bullet
        # as the coordinates of top-left corner for bullet and the tank are different
        bullet.position = fire_position(pos_x, pos_y, direction)

        # add the bullet to the group in order to manage
        self.bullet_group.add(bullet)

        # add one to the bullet on map value of the player
        player.bullet_on_map += 1

        # check the bullet collision immediate, more details in bullet collision function
        self.bullet_collision(bullet, "immediate")

    # movement of the bullet
    def move_bullet(self, bullet):

        # bullet moves once per 30 ticks
        if ticks > bullet.last_move_time + 30:

            # allow the movement of the bullet 30 ticks after the last movement
            bullet.ready_to_move = True

        else:

            # otherwise, stop the position update for the bullet
            bullet.ready_to_move = False

        # bullet direction is a half of the tank direction according to the image sequence
        # (two images for a tank in each direction, but only one image for a bullet in one direction)
        direction = bullet.direction * 2

        # calculate the velocity as a point object based on bullet's moving speed and the firing direction
        velocity = calc_velocity(direction, bullet.speed)

        # x and y component of the velocity
        x = velocity.x
        y = velocity.y

        # detect the collision for the bullet while moving
        if bullet.ready_to_move:

            # moving towards right
            if x > 0:

                # although the minimum moving distance for a bullet in this game is 12 unit pixels
                # bullet collision detection cannot be done for only once in a movement
                # as a distance of 12 pixels is already a huge gap in this game, if the collision detection is based on
                # the starting point and the ending point, bullet may jump through some small environment objects on
                # the map, such a a thin bricks wall
                for i in range(int(x)):

                    # as the bullet is eliminated immediately after a collision
                    # only detect the collision if the bullet is still existing
                    # to prevent unexpected collision
                    if not bullet.exist:

                        # otherwise, stop updating the position of the bullet and break the loop
                        break

                    # add 1 to the x coordinate (scan the next line)
                    bullet.X += 1

                    # way of detection is now call a normal collision detection
                    # which is used to detect the collision when the bullet is moving normally after launching
                    # for the type of collision detection, more details in the bullet collision function below
                    self.bullet_collision(bullet, "normal")

            # same rules apply to the bullet when it is moving in another direction
            # moving towards left
            elif x < 0:
                for i in range(int(-x)):
                    if not bullet.exist:
                        break
                    bullet.X -= 1
                    self.bullet_collision(bullet, "normal")

            # moving towards down
            if y > 0:
                for i in range(int(y)):
                    if not bullet.exist:
                        break
                    bullet.Y += 1
                    self.bullet_collision(bullet, "normal")

            # moving towards up
            elif y < 0:
                for i in range(int(-y)):
                    if not bullet.exist:
                        break
                    bullet.Y -= 1
                    self.bullet_collision(bullet, "normal")

            # when the bullet status is updated, record the updating time to prevent too frequent updates
            bullet.last_move_time = ticks

        # kill the bullet when out of the boundary
        if bullet.X < 0 + 48 or bullet.X > 609 + 48 or bullet.Y < 0 + 24 or bullet.Y > 624 + 24:
            x = bullet.X
            y = bullet.Y

            # reduce the bullet on map for the bullet provider
            if bullet.tank.bullet_on_map > 0:
                bullet.tank.bullet_on_map -= 1

            # kill the bullet and set the existing state to false
            bullet.kill()
            bullet.exist = False

            # create a small explosion
            explosion = Explosion("small")
            explosion.position = x - 48, y - 48
            self.explosion_group.add(explosion)

            # if the bullet is fired by a player
            if bullet.tank.number in [0, 1, 2, 3, 4, 5, 6, 7]:

                # player the sound clip for hitting a steel wall
                play_sound("steel")

    # bullet collision detection function
    # the major function to detect all kinds of collisions between bullets and other objects
    def bullet_collision(self, bullet, collision_type):

        # before the detection process, assume that there is no collision taking place
        overall_collision = False

        # collisions with bricks wall
        collision_bricks = pygame.sprite.spritecollideany(bullet, self.bricks_group)

        # if a collision or multiply collisions happen(s)
        if collision_bricks:

            # no longer assume that no collision taking place
            overall_collision = True

            # save the bullet position as x and y coordinates as the bullet may be killed before its position being
            # used again
            x = bullet.X
            y = bullet.Y

            # create a small explosion based on the hitting position
            explosion = Explosion("small")
            explosion.position = x - 48, y - 48
            self.explosion_group.add(explosion)

            # if the bullet is fired by a player
            if bullet.tank.number in [0, 1, 2, 3, 4, 5, 6, 7]:

                # player the sound clip for hitting the brick
                play_sound("brick")

            # save the direction of the bullet as well
            direction = bullet.direction

            # kill the bullet and turn the existing state to False to prevent further collision
            bullet.kill()
            bullet.exist = False

            # a, b are the position adjustment for the bullet in order to create a further sprite to detect which
            # bricks need to be eliminated on the map
            a, b = 0, 0

            # if the bullet is fired vertically
            if direction == 0 or direction == 2:

                # if it is moving upwards
                if direction == 0:

                    # there are two types of bullet collision, as bullets are the fastest moving object in this game

                    # normal collision detection is used for bullets in normal moving
                    if collision_type == "normal":
                        a, b = -18, -9

                    # if the player is shooting right in front of a brick wall or a steel wall
                    # a immediate collision based on the initial position of the bullet is set up
                    # as if the bullet if moving at the first place, it may eliminate the next line of objects in front
                    # of it instead of the ideal ones
                    elif collision_type == "immediate":
                        a, b = -18, 0

                # if the bullet is fired downwards, same rules apply
                elif direction == 2:
                    if collision_type == "normal":
                        a, b = -18, 18
                    elif collision_type == "immediate":
                        a, b = -18, 9

                # as the tier 4 tank eliminate two lines of bricks at a time
                if bullet.tank.number in [3, 7]:

                    # a further adjustment is applied
                    if direction == 0:
                        b -= 6
                    elif direction == 2:
                        pass

                # temp is the sprite used to detect the bricks that need to be eliminated
                temp = StaticSprite()

                # if the tank is a tier 4 tank, a thicker detecting area needs to be considered
                if bullet.tank.number in [3, 7]:
                    temp.load("images/environment.png", 48, 11, 0, 0)

                # tier 1, 2 or 3 tanks have normal detecting area
                else:
                    temp.load("images/environment.png", 48, 3, 0, 0)

                # temp position is the combination of bullet position and the adjustment
                temp.position = x + a, y + b

                # go through the bricks list
                for bricks in self.bricks_group.sprites():

                    # if the brick is colliding with the temp sprite
                    if pygame.sprite.collide_rect(bricks, temp):

                        # kill the brick
                        bricks.kill()

                # and the temp sprite
                temp.kill()

            # when the bullet is moving horizontally, same rules apply
            if direction == 1 or direction == 3:

                # bullet moves towards left
                if direction == 1:
                    if collision_type == "normal":
                        a, b = -9, -21
                    elif collision_type == "immediate":
                        a, b = 0, -21

                # bullet moves towards right
                elif direction == 3:
                    if collision_type == "normal":
                        a, b = 18, -21
                    elif collision_type == "immediate":
                        a, b = 9, -21

                if bullet.tank.number in [3, 7]:
                    if direction == 1:
                        a -= 6
                    elif direction == 3:
                        pass

                temp = StaticSprite()

                if bullet.tank.number in [3, 7]:

                    # when the bullet is fired horizontally,
                    # detecting area has a greater height than width
                    temp.load("images/environment.png", 11, 48, 0, 0)

                else:
                    temp.load("images/environment.png", 3, 48, 0, 0)
                temp.position = x + a, y + b

                for bricks in self.bricks_group.sprites():
                    if pygame.sprite.collide_rect(bricks, temp):
                        bricks.kill()
                temp.kill()

        # collisions with steel wall
        collision_steel = pygame.sprite.spritecollideany(bullet, self.wall_group)

        # if the bullets collide with the steel wall
        if collision_steel:

            # assume that the collision happens
            overall_collision = True

            # save the bullet position in case it is used after being killed
            x = bullet.X
            y = bullet.Y

            # create a small explosion on the hitting position
            explosion = Explosion("small")
            explosion.position = x - 48, y - 48
            self.explosion_group.add(explosion)

            # play the sound clip of hitting a steel wall if the bullet is fired by a player
            if bullet.tank.number in [0, 1, 2, 3, 4, 5, 6, 7]:
                play_sound("steel")

            # save the direction of the bullet in case being used after the bullet is killed
            direction = bullet.direction

            # kill the bullet and change the existing state
            bullet.kill()
            bullet.exist = False

            # if the player is a tier 4 tank
            # (only tier 4 tank can eliminate steel wall on the map)
            if bullet.tank.number in [3, 7]:

                # same idea as the collision with bricks wall
                # the difference is that a square unit of steel wall is made up of 4 pieces of steel in a
                # 2x2 matrix, the bullet eliminates a line of steel at a time
                a, b = 0, 0
                if direction == 0 or direction == 2:
                    if direction == 0:
                        if collision_type == "normal":
                            a, b = -18, -9
                        elif collision_type == "immediate":
                            a, b = -18, 0
                    elif direction == 2:
                        if collision_type == "normal":
                            a, b = -18, 18
                        elif collision_type == "immediate":
                            a, b = -18, 9
                    temp = StaticSprite()

                    # testing area is the same with the one used for a line of bricks as a line of steel (2 pieces)
                    # will also be detected
                    temp.load("images/environment.png", 48, 3, 0, 0)
                    temp.position = x + a, y + b

                    # go through the steel in the group
                    for steel in self.wall_group.sprites():

                        # kill the steel if collision happens
                        if pygame.sprite.collide_rect(steel, temp):
                            steel.kill()
                    temp.kill()

                # exact the same idea for bullet traveling horizontally
                if direction == 1 or direction == 3:
                    if direction == 1:
                        if collision_type == "normal":
                            a, b = -9, -21
                        elif collision_type == "immediate":
                            a, b = 0, -21
                    elif direction == 3:
                        if collision_type == "normal":
                            a, b = 18, -21
                        elif collision_type == "immediate":
                            a, b = 9, -21
                    temp = StaticSprite()
                    temp.load("images/environment.png", 3, 48, 0, 0)
                    temp.position = x + a, y + b

                    for steel in self.wall_group.sprites():
                        if pygame.sprite.collide_rect(steel, temp):
                            steel.kill()
                    temp.kill()

        # collisions with other bullets
        collision_bullet = []

        # as the bullet is always colliding with itself which causes a problem, a list includes all the other bullets
        # needs to be created at the first place
        for other_bullet in self.bullet_group.sprites():

            # detect the collision between the bullet and "the other bullet" only if they are different
            if bullet != other_bullet:
                collision = pygame.sprite.collide_rect(bullet, other_bullet)

                # if the a collision happens
                if collision:

                    # assume that collision happens
                    overall_collision = True

                    # add the the colliding bullet to the list in order to manage
                    collision_bullet.append(other_bullet)

        # when there is another bullet in the colliding list
        if collision_bullet:

            # kill the bullet and change its state
            bullet.kill()
            bullet.exist = False

            # go through the list of bullets being collided
            for other_bullet in collision_bullet:

                # reduce one from bullet on map of the other bullet's owner as the other bullet is now killed and
                # its collision state will not be detected for the other time
                other_bullet.tank.bullet_on_map -= 1

                # kill the other bullet and change its state
                other_bullet.kill()
                other_bullet.exist = False

        # collisions with enemy tanks
        # detect the collision between bullet and enemies if the bullet is fired by a player
        if bullet.tank.number in [0, 1, 2, 3, 4, 5, 6, 7]:

            # all the hit enemies are returned to the attacked list
            attacked = pygame.sprite.spritecollide(bullet, self.enemy_group, True)

            # assume that collision takes place if there is a collision
            if attacked:
                overall_collision = True

                # delete the enemy which is attacked
                for enemy in attacked:

                    # if the attacked enemy is a basic tank
                    if type(enemy) == BasicTank:

                        # add 100 points to player's score
                        self.score += 100

                        # add one to the basic tank elimination counter
                        self.eliminate_basic += 1

                    # same as above is the enemy is a fast tank or a power tank
                    elif type(enemy) == FastTank:
                        self.score += 200
                        self.eliminate_fast += 1
                    elif type(enemy) == PowerTank:
                        self.score += 300
                        self.eliminate_power += 1

                    # remove the enemy from the on map enemies list
                    # check before removing in case there's an error
                    if enemy in self.enemy_list:
                        self.enemy_list.remove(enemy)

                        # get the position of the eliminated tank
                        x, y = enemy.position

                        # create a large explosion on the position of the eliminated tank
                        explosion = Explosion("large")
                        explosion.position = x - 24, y - 24
                        self.explosion_group.add(explosion)

                        # play the sound clip for explosion
                        play_sound("explosion")

                        # subtract one from the enemy on map counter (which is used to prevent over-spawning enemies)
                        self.enemy_on_map -= 1

                    # if the enemy is a award type enemy, spawn a power-up on the map
                    if enemy.enemy_type % 2 == 1:
                        self.spawn_powerup()

                # record the last elimination time to prevent the program from spawning enemies at an unexpected rate
                self.last_elimination_time = ticks

                # save the bullet position in case using after killing
                x = bullet.X
                y = bullet.Y

                # kill the bullet and change its state
                bullet.kill()
                bullet.exist = False

                # create a large explosion
                explosion = Explosion("small")
                explosion.position = x - 48, y - 48
                self.explosion_group.add(explosion)

            # collision with armor
            # as armor tank has four lives, it has a slightly different collision function
            attacked = pygame.sprite.spritecollide(bullet, self.armor_tank_group, False)

            # if collision happens
            if attacked:

                # set the collision state to true
                overall_collision = True

                # save the bullet position for later use
                x = bullet.X
                y = bullet.Y

                # kill the bullet and change its state
                bullet.kill()
                bullet.exist = False

                # go through the list to apply change on each armor tank
                for armor_tank in attacked:

                    # as bullet is moving fast and the bullet collision function detects collision very often
                    # one bullet may case more than one harm to a armor tank
                    # each time if the armor tank is hit by a bullet, this bullet is recorded in order to reduce error
                    if bullet not in armor_tank.hit_by:

                        # if the armor tank is a award armor tank and this is the first time of it being hit
                        if armor_tank.enemy_type == 7 and armor_tank.life == 4:

                            # spawn a power-up on the map
                            self.spawn_powerup()

                        # reduce one to the armor tank lives
                        armor_tank.life -= 1

                        # if the armor tank has no life left
                        if armor_tank.life == 0:

                            # kill the armor tank
                            armor_tank.kill()

                            # remove it from the on map enemy list
                            if armor_tank in self.enemy_list:
                                self.enemy_list.remove(armor_tank)

                                # add 400 points to the player's score and add one to the elimination counter
                                self.score += 400
                                self.eliminate_armor += 1

                                # record the tanks position
                                x_2, y_2 = armor_tank.position

                                # create an explosion above the armor tank
                                explosion = Explosion("large")
                                explosion.position = x_2 - 24, y_2 - 24
                                self.explosion_group.add(explosion)

                                # play the sound clip for explosion
                                play_sound("explosion")

                                # record the elimination time and reduce one to the on map enemy counter
                                self.last_elimination_time = ticks
                                self.enemy_on_map -= 1

                        # record the bullet in armor tank's hit be list
                        armor_tank.hit_by.append(bullet)

                # create a small explosion no matter the armor tank is eliminated on where bullet hit the armor tank
                explosion = Explosion("small")
                explosion.position = x - 48, y - 48
                self.explosion_group.add(explosion)

        # collisions with player tanks
        # detect the collision between players and bullet fired by enemy
        if bullet.tank.number == 8:

            # collided player will be return to the attacked list
            # False means not to kill the player now
            attacked = pygame.sprite.spritecollide(bullet, self.player_group, False)

            # if there is something in the attacked list
            if attacked:

                # change the collision state for this detection
                overall_collision = True

                # go through the attacked list to apply effect on each player
                for player in attacked:

                    # record the position of the player for later use
                    x = bullet.X
                    y = bullet.Y

                    # kill the bullet and change its state
                    bullet.kill()
                    bullet.exist = False

                    # if the player is matchless, which is a state that cannot be eliminated
                    if player.spawn_matchless or player.powerup_matchless:

                        # create a small explosion on where the bullet hit the player
                        explosion = Explosion("small")
                        explosion.position = x - 48, y - 48
                        self.explosion_group.add(explosion)

                    # when the player is not matchless
                    else:

                        # kill the player sprite
                        player.kill()

                        # kill the previous matchless sprite for the player as well
                        self.matchless_sprite.kill()

                        # reduce one to the player life counter
                        self.player_life -= 1

                        # record the elimination time in order to create another player later
                        self.last_player_elimination_time = ticks

                        # if the player has no life left
                        if self.player_life == -1:

                            # enter the game over status
                            self.game_over = True

                            # record the game over time to allow more change on the screen later
                            self.game_over_time = ticks

                            # create the game over text object to show it on the screen
                            game_over = GameOver()

                            # add the game over text object to the group in order to update and manage
                            self.game_over_text_group.add(game_over)

                        # set the player tank to nothing
                        self.player_tank = None

                        # record the player's position in order to create explosion
                        x_2, y_2 = player.position

                        # create a large explosion above the player
                        explosion = Explosion("large")
                        explosion.position = x_2 - 24, y_2 - 24
                        self.explosion_group.add(explosion)

                        # play the sound clip for explosion
                        play_sound("explosion")

                        # create a small explosion on where the bullet hit the player
                        explosion = Explosion("small")
                        explosion.position = x - 48, y - 48
                        self.explosion_group.add(explosion)

        # collision with eagle pattern
        # if the eagle in the base is killed, no matter how many lives has player had left, game overs
        eagle_collision = pygame.sprite.spritecollide(bullet, self.eagle_group, False)

        # if the eagle is hit
        if eagle_collision:

            # and if the game is not already over as there is no need for the detection any more
            if not self.game_over:

                # change the collision state
                overall_collision = True

                # save the bullet position for later use
                x = bullet.X
                y = bullet.Y

                # create a small explosion on where it is hit by the bullet
                explosion = Explosion("small")
                explosion.position = x - 48, y - 48
                self.explosion_group.add(explosion)

                # kill the bullet
                bullet.kill()
                bullet.exist = False

                # go through the eagle attacked list
                for eagle in eagle_collision:

                    # kill the eagle pattern
                    eagle.kill()

                # dead eagle also have a pattern
                dead_eagle = StaticSprite()
                dead_eagle.load("images/environment.png", 48, 48, 96, 48)
                dead_eagle.position = 288 + 48, 576 + 24

                # create a large explosion above the eagle
                explosion = Explosion("large")
                explosion.position = 288 + 24, 576
                self.explosion_group.add(explosion)

                # play the sound clip for the explosion
                play_sound("explosion")

                # add the dead eagle pattern to the group in order to update and manage
                self.eagle_group.add(dead_eagle)

                # enter the game over status
                self.game_over = True

                # record the game over time in order to switch to another screen and show the text later
                self.game_over_time = ticks

                # create the game over text object and add it to the group
                game_over = GameOver()
                self.game_over_text_group.add(game_over)

        # if there is a collision happened during this detection, one is reduced from the bullet on map counter
        if overall_collision:

            # check to reduce the error
            if bullet.tank.bullet_on_map > 0:

                # reduce one to the bullet on map counter of the bullet's owner
                bullet.tank.bullet_on_map -= 1

    # create a power-up on a random position on the map
    def spawn_powerup(self):

        # type of the power up is also randomly generated
        powerup_type = random.randint(0, 5)

        powerup = None

        # when the type number is 0, generate a grenade on the map
        if powerup_type == 0:
            powerup = Grenade()

        # same as above to generate the other power-ups
        elif powerup_type == 1:
            powerup = Helmet()
        elif powerup_type == 2:
            powerup = Shovel()
        elif powerup_type == 3:
            powerup = Star()
        elif powerup_type == 4:
            powerup = Tank()
        elif powerup_type == 5:
            powerup = Timer()

        # load the master image for the power-up sprite as it is a dynamic sprite
        powerup.load("images/power_ups.png", 48, 48, 2)

        # although power-up is generated on map at a random position
        # there is still some place not suitable for generating a power-up
        # for example, water, which is a not achievable position for the player on the map
        valid_position = False

        # find another place continuously if the position isn't suitable
        while not valid_position:

            # generate a pair of coordinates as the position for the power-up
            x = random.randint(48, 624)
            y = random.randint(24, 600)

            # place the power-up
            powerup.position = x, y

            # detect the collision between power-up and water and eagle sprite
            on_water = pygame.sprite.spritecollide(powerup, self.water_group, False)
            on_eagle = pygame.sprite.spritecollide(powerup, self.eagle_group, False)

            # if the power-up is spawned on a valid position
            if not on_water and not on_eagle:

                # validate the power-up generation
                valid_position = True

        # add the power-up to the group in order to update and manage
        self.powerup_group.add(powerup)

    # determine whether player is colliding with a power-up
    def player_collision(self, player):

        # collision will be a list returned which includes the collied power-ups
        # True allows the function to kill the power-up directly after the collision
        collision = pygame.sprite.spritecollide(player, self.powerup_group, True)

        # when the player is colliding with a power-up
        if collision:

            # play the bonus sound clip
            play_sound("bonus")

            # add 500 points to player's score
            self.score += 500

            # apply the power-up to the player or to the game based on which power-up has collied with the player
            for powerup in collision:

                # if the player touches a grenade power-up
                if type(powerup) == Grenade:

                    # apply the grenade power-up
                    powerup.grenade(self)

                # same as above
                elif type(powerup) == Helmet:
                    powerup.helmet(self, player)

                elif type(powerup) == Shovel:
                    powerup.shovel(self)

                elif type(powerup) == Star:
                    powerup.star(player, self)

                elif type(powerup) == Tank:
                    powerup.tank(self)

                elif type(powerup) == Timer:
                    powerup.timer(self)

    # check and end the matchless when necessary
    def end_matchless(self):

        # when the matchless is a automatic matchless after spawn
        if self.player_tank.spawn_matchless:

            # matchless only apply for 4000 ticks in this case
            if ticks > self.player_tank.last_spawn_matchless_time + 4000:

                # kill the matchless when time is out
                self.matchless_sprite.kill()
                self.player_tank.spawn_matchless = False

            # update the matchless if it is still applied
            else:

                # place the matchless sprite right on the player sprite
                x, y = self.player_tank.position
                self.matchless_sprite.position = x, y

        # same rules apply for a power-up matchless
        # power-up matchless lasts longer than a spawn matchless
        elif self.player_tank.powerup_matchless:
            if ticks > self.player_tank.last_powerup_matchless_time + 15000:
                self.matchless_sprite.kill()
                self.player_tank.powerup_matchless = False
            else:
                x, y = self.player_tank.position
                self.matchless_sprite.position = x, y

    # end the shovel for the base when time is out
    def end_shovel(self):

        # shovel only needs to be end if a shovel is applied to the game
        if self.shoveled:

            # when 20000 ticks have passed after the applying of a shovel
            if ticks > self.last_shovel_time + 20000:

                # remove the sprites (bricks or steel) which make up the base from both base group and
                # the wall or bricks group to stop the update and the iteractions
                for sprite in self.base_group.sprites():
                    sprite.kill()

                # build the base completely using bricks again
                self.base_builder("bricks")

                # switch back to the normal state
                self.shoveled = False

    # end the timer when time is out
    # basics rules are the same as above
    def end_timer(self):
        if ticks > self.last_timer_time + 15000:
            self.apply_timer = False

    # check if the player is successful
    def check_success(self):

        # if the elimination all state hasn't been set to active
        if not self.elimination_all:

            # if there is no more left in enemy spawn list
            if not self.enemy_spawn_list:

                # and no more enemy left on the map
                if self.enemy_on_map == 0:

                    # set the elimination all state to active
                    self.elimination_all = True

                    # record the time for further effects
                    self.elimination_all_time = ticks

        # game is success 2000 ticks after eliminating all the enemies
        if self.elimination_all:
            if ticks > self.elimination_all_time + 2000:
                self.success = True

    # update the status of all the sprites involved
    def update(self):

        # most of the sprites in the groups have a fixed refreshing frequency
        self.bricks_group.update(ticks, 30)
        self.wall_group.update(ticks, 30)

        # water flashes per 600 ticks
        self.water_group.update(ticks, 600)
        self.trees_group.update(ticks, 30)
        self.ice_group.update(ticks, 30)
        self.base_group.update(ticks, 30)
        self.eagle_group.update(ticks, 30)
        self.counter_group.update(ticks, 30)
        self.flag_group.update(ticks, 30)
        self.player_counter_group.update(ticks, 30)
        self.game_over_text_group.update(ticks, 30)
        self.player_group.update(ticks, 30)
        self.matchless_group.update(ticks, 30)
        self.enemy_group.update(ticks, 30)
        self.armor_tank_group.update(ticks, 30, 10)

        # power-ups flash per 360 ticks
        self.powerup_group.update(ticks, 360)
        self.bullet_group.update(ticks, 30)

        # explosion has a special update function, go through all the explosions and apply the update function
        for explosion in self.explosion_group.sprites():
            explosion.explode(ticks, 120)

    # draw the updates
    def draw(self):

        # fill the screen with grey background
        screen.fill((127, 127, 127))

        # draw a black square as the battlefield of the game
        pygame.draw.rect(screen, (0, 0, 0), (48, 24, 624, 624), 0)

        # draw all the sprites on the screen
        # sprites that are drawn at last will be above the sprites that were drawn at the begining
        self.bricks_group.draw(self.screen)
        self.wall_group.draw(self.screen)
        self.water_group.draw(self.screen)
        self.ice_group.draw(self.screen)
        self.eagle_group.draw(self.screen)
        self.counter_group.draw(self.screen)
        self.flag_group.draw(self.screen)
        self.player_counter_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.matchless_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.armor_tank_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.explosion_group.draw(self.screen)
        self.trees_group.draw(self.screen)
        self.powerup_group.draw(self.screen)
        self.game_over_text_group.draw(self.screen)

    # run the next step for the game
    def run(self):

        # global some variables from out side as the game need to save some info. for the next level
        global status, board, score, player_1, life

        if self.initialize:

            # build the environment
            self.map_loader()
            self.base_builder("bricks")
            self.eagle_builder()

            # load the enemy list which includes the order of spawning enemies
            self.enemy_spawn_list_loader()

            # load a few more sprites on the right grey edge
            self.enemy_counter_loader()
            self.flag_loader()
            self.player_counter_loader()

            # initialize the last elimination time a last spawn time
            self.last_elimination_time = ticks
            self.last_spawn_time = ticks

            # load the player tank from previous game
            self.player_tank_loader(self.player_tank)
            self.player_tank.bullet_on_map = 0

            # end the initialization process
            self.initialize = False

        elif self.game_over:

            # switch to scoring board when certain time is passed
            if ticks > self.game_over_time + 4000:
                score += self.score
                status = "board"
                board = Board(self.screen, self)

            # when not need to switch to the board
            else:

                # rise the game over text
                for sprite in self.game_over_text_group.sprites():
                    if sprite.Y > 312:
                        sprite.Y -= 8

                # update and draw the next stage for the game
                self.update()
                self.draw()

                # all the other parts runs as normal
                # apart from which player cannot move
                self.load_enemy()

                if not self.apply_timer:
                    for enemy in self.enemy_list:
                        self.move_enemy(enemy)
                else:
                    for enemy in self.enemy_list:
                        enemy.first_frame = enemy.last_frame = enemy.frame

                for bullet in self.bullet_group.sprites():
                    self.move_bullet(bullet)

        # when the player wins
        elif self.success:

            # add the score gaining during this level to the universal score
            score += self.score

            # save the player tank for the next level
            player_1 = self.player_tank

            # save the remaining lives for the next level
            life = self.player_life

            # switch to the scoring board
            status = "board"
            board = Board(self.screen, self)

        # when player is eliminated
        elif not self.player_tank:

            # load the player again a certain time after the elimination
            if ticks > self.last_player_elimination_time + 2000:

                # only load the player again if it is not completely dead
                if self.player_life > -1:
                    self.player_tank_loader(PlayerTank(0))
                    self.player_tank.bullet_on_map = 0

            # refresh the player live counter
            self.player_counter_loader()

            # all the other parts of the game run as normal
            self.load_enemy()

            self.end_shovel()
            self.end_timer()

            if not self.apply_timer:

                for enemy in self.enemy_list:
                    self.move_enemy(enemy)

            for bullet in self.bullet_group.sprites():
                self.move_bullet(bullet)

            # update and draw the next stage of the game
            self.update()
            self.draw()

        # when the game is running as normal
        else:

            # update and draw the next stage of the game
            self.update()
            self.draw()

            # check whether player wins
            self.check_success()

            # load the enemy on the map when necessary
            self.load_enemy()

            # detect the collisions between players and power-ups
            self.player_collision(self.player_tank)

            # end the power-ups when necessary
            self.end_shovel()
            self.end_matchless()
            self.end_timer()

            # move the enemies when timer is not applied
            if not self.apply_timer:
                for enemy in self.enemy_list:
                    self.move_enemy(enemy)

            # freeze the enemies and stop the
            else:
                for enemy in self.enemy_list:
                    enemy.first_frame = enemy.last_frame = enemy.frame

            # move the player
            # player sometimes becomes a none-type which is an unsolved mystery
            # try function skip the errors as it happens rarely and one tiny moment of moving
            # problem is better than interrupting the whole game
            try:
                self.move_player(self.player_tank)
            except():
                pass

            # remove the power-ups on the map when time is out
            for powerup in self.powerup_group.sprites():
                powerup.time_out(ticks)

            # move the bullets
            for bullet in self.bullet_group.sprites():
                self.move_bullet(bullet)


# Menu object is the starting menu of the Battle City
class Menu(object):

    # initialize Menu class
    def __init__(self, pygame_screen):

        # get the screen for the game
        self.screen = pygame_screen

        # default choice is single player
        self.choice = 0

        # last rising time is used to control the rising of the background image
        self.last_rising_time = 0

        # set the menu to initializing mode
        self.initializing = True

        # set up the pointer
        self.pointer = None

        # create the groups to manage the sprites
        self.pointer_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()

        # create the background as a StaticSprite
        self.background = MenuImage()
        self.background_group.add(self.background)

    # function to rise the background image
    def initialize(self):

        # global release to get the keys being released at a certain time
        global release

        # quickly place the background image to the ready position if enter is released
        if "RETURN" in release:
            self.background.Y = 0

        # otherwise, slowly rise the background image
        if ticks > self.last_rising_time + 30:
            self.last_rising_time = ticks

            # when the background image reached the ready position, end the initializing
            if self.background.Y == 0:
                self.initializing = False

                # load the tank image as a pointer as well
                self.load_pointer()

            # rise the background
            else:
                self.background.Y -= 8

    # load a tank sprite as a pointer for the menu
    def load_pointer(self):

        # create and initialize the sprite for the pointer
        tank = PlayerTank(0)
        tank.load("images/tanks.png", 48, 48, 8)
        tank.frame = 6
        tank.first_frame = 6
        tank.last_frame = 7
        tank.position = 192, 369

        # set the sprite as the pointer
        self.pointer = tank

        # add the pointer to the group in order to manage
        self.pointer_group.add(self.pointer)

    # place the pointer at the right position when the choice is changed
    def place_pointer(self):

        # choice 0 (single player) means pointer at the position 192, 369
        if self.choice == 0:
            self.pointer.position = 192, 369

        # same applies as above
        elif self.choice == 1:
            self.pointer.position = 192, 417
        elif self.choice == 2:
            self.pointer.position = 192, 465

    # move down the pointer
    def move_down(self):
        self.choice += 1

        # when the choice is too large, pull it back
        if self.choice == 3:
            self.choice = 0

        # move the pointer after changing choice
        self.place_pointer()

    # same as above
    def move_up(self):
        self.choice -= 1
        if self.choice == -1:
            self.choice = 2
        self.place_pointer()

    # move the pointer based on the key board events
    def move_pointer(self):

        # keyboards event and changing states are controlling by outside variables
        global keys, release, status, level

        # move down if "s" key is released
        if "s" in release:
            self.move_down()

        # same as above
        elif "w" in release:
            self.move_up()

        # enter the "level" status if the player has released the enter
        elif keys[K_RETURN]:
            status = "level"
            level = Level(self.screen, 1, True)

    # update the groups
    def update(self):
        self.background_group.update(ticks, 30)
        self.pointer_group.update(ticks, 60)

    # draw the sprites in the groups on the given screen
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.background_group.draw(self.screen)
        self.pointer_group.draw(self.screen)

    # run the starting menu screen
    def run(self):

        # when the background is not ready
        if self.initializing:

            # rise the background
            self.initialize()

            # update and draw the sprites
            self.update()
            self.draw()

        # when the background is ready
        if not self.initializing:

            # wait for the keyboard events
            self.move_pointer()

            # update and draw the sprites
            self.update()
            self.draw()


# Level object controls the level choosing menu
class Level(object):

    # initialize Level class
    def __init__(self, pygame_screen, choice, choose):

        # get the screen for the level choosing menu
        self.screen = pygame_screen

        # fill the screen with black to cover the menu
        self.screen.fill((0, 0, 0))

        # filling height is used to form a window closing or opening effects
        self.filling_height = 0

        # choice is the level that the player is choosing
        self.choice = choice

        # last painting time prevent the level object from have a high refreshing rate
        self.last_painting_time = 0

        # unknown
        self.last_spawn_time = ticks

        # set the level to initializing mode
        self.initializing = True

        # clear is used to clear level choosing screen and load the real game
        self.clearing = False
        self.cleared = False

        # when enter the level choosing windows for the first time, changing level is allowed
        # but level is not allowed to be changed when player is going to load the next level
        self.allow_change = choose

        # text is the "STAGE" text on the screen
        self.text = None

        # numbers are the number of stage on the screen
        self.number_1 = None
        self.number_2 = None

        # create the text group
        self.text_group = pygame.sprite.Group()

    def initialize(self):

        # stop filling the screen when the whole screening is filled
        # load the text and the numbers when the screen filling finished
        if self.filling_height >= 336:
            self.initializing = False
            self.filling_height = 336

            # load the letters and place them in the right position
            self.text = StaticSprite()
            self.text.load("images/letters.png", 120, 24, 0, 0)
            self.text.position = 288, 324
            self.text_group.add(self.text)

            # load the numbers and place them in the right position
            num_2 = self.choice % 10
            self.number_2 = Number(num_2)
            self.number_2.position = 456, 324
            self.text_group.add(self.number_2)

            # single digit number doesn't have a secondary digit
            # load the secondary digit when necessary
            num_1 = self.choice // 10
            if num_1 != 0:
                self.number_1 = Number(num_1)
                self.number_1.position = 432, 324
                self.text_group.add(self.number_1)

        # when the screen is not fully filled, fill the screen
        else:

            # changing the filling height only if a certain period of time is passed
            if ticks > self.last_painting_time + 30:

                # record the new filling time in order to calculate the time gap
                self.last_painting_time = ticks

                # increase the filling height
                self.filling_height += 96

            # filling the screen using two rectangles with grey color
            block_color = 127, 127, 127
            pos_1 = 0, 0, 768, self.filling_height
            pos_2 = 0, 672 - self.filling_height, 768, self.filling_height

            # draw the rectangles
            pygame.draw.rect(self.screen, block_color, pos_1, 0)
            pygame.draw.rect(self.screen, block_color, pos_2, 0)

    # function to clear the screen when the filling process finished
    # and need to load the new level
    def clear_screen(self):

        # when the grey part is not fully cleared
        # notice that 24 unit pixels of grey edges still remain on the screen
        if self.filling_height > 24:

            # fill the screen with certain shape only if a period of time has passed
            if ticks > self.last_painting_time + 30:
                self.last_painting_time = ticks
                self.filling_height -= 96

            # before filling the screen using rectangles,
            # fill the screen with grey background and draw a black square
            # to pretend there is a battlefield under the curtain
            block_color = 127, 127, 127
            self.screen.fill(block_color)
            pygame.draw.rect(self.screen, (0, 0, 0), (48, 24, 624, 624), 0)

            # draw the two grey retangles
            pos_1 = 0, 0, 768, self.filling_height
            pos_2 = 0, 672-self.filling_height, 768, self.filling_height
            pygame.draw.rect(self.screen, block_color, pos_1, 0)
            pygame.draw.rect(self.screen, block_color, pos_2, 0)

        # when the clearing process is done
        else:

            # set the state as cleared
            self.cleared = True

    # choose precious level
    def move_down(self):

        # subtract 1 from choice
        self.choice -= 1

        # do not allow level change when underflow
        if self.choice == 0:
            self.choice = 1

    # same as above
    def move_up(self):
        self.choice += 1
        if self.choice == 36:
            self.choice = 35

    # change the level based on keyboard events
    def change_level(self):

        # get the keyboard events from outside variables
        global keys, release

        if release:

            # is "s" key is released
            if "s" in release:

                # move down the choice
                self.move_down()
                print(self.choice)

            # same as above
            elif "w" in release:
                self.move_up()
                print(self.choice)

            # when enter is released
            elif "RETURN" in release:

                # play the game starting sound
                play_sound("gamestart")

                # start the clearing process
                self.clearing = True

            # empty text group to remove the previous stage number and load the new stage number
            self.text_group.empty()
            self.text_group.add(self.text)

            # number loading process is again same with above
            num_2 = self.choice % 10
            self.number_2 = Number(num_2)
            self.number_2.position = 456, 324
            self.text_group.add(self.number_2)

            num_1 = self.choice // 10
            if num_1 != 0:
                self.number_1 = Number(num_1)
                self.number_1.position = 432, 324
                self.text_group.add(self.number_1)

    # run the level choosing menu by applying the next stage
    def run(self):

        # need to change some universal variables as a new game state is created straight after
        global status, game

        # fill the screen when the screen needs to be filled
        if self.initializing:
            self.initialize()

        # clear the screen when the screen needs to be cleared
        elif self.clearing:

            # when the whole screen is cleared
            if self.cleared:

                # create a game object where choice of the level is passed through
                game = Game(self.screen, self.choice)

                # change the universal status to "game"
                status = "game"

            # when the screen is not cleared yet
            else:

                # clear the screen
                self.clear_screen()

        # otherwise, remain the stage choosing menu, may allow change level
        else:

            # when changing level is allowed
            if self.allow_change:

                # apply change the level function
                self.change_level()

            # otherwise,
            else:

                # when a certain period of time is passed
                if ticks > self.last_spawn_time + 2000:

                    # clear the screen and play the game starting sound clip
                    self.clearing = True
                    play_sound("gamestart")

            # fill the screen with grey background, update and draw
            self.screen.fill((127, 127, 127))
            self.text_group.update(ticks, 30)
            self.text_group.draw(self.screen)


# Board object controls the scoring board after the end of each level
class Board(object):

    # initialize Board class
    def __init__(self, pygame_screen, last_game):

        # get the screen for the board
        self.screen = pygame_screen

        # get the previous game object as a few variables in the previous game will be used
        self.game = last_game

        # set the board to initializing mode
        self.initializing = True

        # record the spawn time of the board in order to apply the update at a certain time
        self.spawn_time = ticks

        # create groups to manage the sprites used in board object
        self.background_group = pygame.sprite.Group()
        self.basic_number_group = pygame.sprite.Group()
        self.fast_number_group = pygame.sprite.Group()
        self.power_number_group = pygame.sprite.Group()
        self.armor_number_group = pygame.sprite.Group()
        self.other_number_group = pygame.sprite.Group()

        # game over sound played is used to make sure the game over sound is only played once
        self.game_over_sound_played = False

        # last appear order is used to paint and change the scores on the screen
        self.last_appear_order = 0

        # elimination list is loaded based on the previous game to show the result of the game
        self.elimination_list = []

        # when there is basic tank being killed
        if self.game.eliminate_basic > 0:
            for i in range(self.game.eliminate_basic):

                # add a "B" to the elimination list
                self.elimination_list.append("B")

        # if no basic tank is killed
        else:

            # a "BX" which means no basic tank killed is appended
            # as 0 kill, 0 score also need to be represented on the screen
            # and showing 0 also counts for a update
            self.elimination_list.append("BX")

        # same rules apply for fast, power and armor tanks
        if self.game.eliminate_fast > 0:
            for i in range(self.game.eliminate_fast):
                self.elimination_list.append("F")
        else:
            self.elimination_list.append("FX")

        if self.game.eliminate_power > 0:
            for i in range(self.game.eliminate_power):
                self.elimination_list.append("P")
        else:
            self.elimination_list.append("PX")

        if self.game.eliminate_armor > 0:
            for i in range(self.game.eliminate_armor):
                self.elimination_list.append("A")
        else:
            self.elimination_list.append("AX")

        # set up counter to control the time as number of kills and score flicker
        self.basic_counter = 0
        self.fast_counter = 0
        self.power_counter = 0
        self.armor_counter = 0

    # function to update all the sprites in the groups
    def update(self):
        self.background_group.update(ticks, 30)
        self.basic_number_group.update(ticks, 30)
        self.fast_number_group.update(ticks, 30)
        self.power_number_group.update(ticks, 30)
        self.armor_number_group.update(ticks, 30)
        self.other_number_group.update(ticks, 30)

    # function to paint the sprites in the screen
    def draw(self):
        self.background_group.draw(self.screen)
        self.basic_number_group.draw(self.screen)
        self.fast_number_group.draw(self.screen)
        self.power_number_group.draw(self.screen)
        self.armor_number_group.draw(self.screen)
        self.other_number_group.draw(self.screen)

    def run(self):

        # universal variables need to be changed as a new level or game over is following
        # the scoring board
        global status, level, menu, score

        # when initializing the scoring board
        if self.initializing:

            # load and place the background of the board as a StaticSprite
            background = StaticSprite()
            background.load("images/board_s.png", 768, 672, 0, 0)
            background.position = 0, 0
            self.background_group.add(background)

            # print high score, game level and score gained in the previous level on the screen
            print_number(20000, "yellow", 576, 48, self.other_number_group)
            print_number(self.game.level, "white", 480, 96, self.other_number_group)
            print_number(score, "yellow", 264, 192, self.other_number_group)
            self.initializing = False

            # update and draw the sprites
            self.update()
            self.draw()

        # when the initialization finishes
        else:

            # time gap is the gap between each flickering
            time_gap = 200

            # total number of gaps required to load all the flickering numbers is base on
            # the elimination number from the previous level
            total = len(self.elimination_list)

            # when a certain time is passed
            if ticks > self.spawn_time + (total + 18) * time_gap:

                # if the player won the previous game
                if self.game.success:

                    # get into the next level
                    status = "level"
                    level = Level(self.screen, self.game.level+1, False)

                # if player lost the previous game
                elif self.game.game_over:

                    # when a certain time is passed
                    if ticks > self.spawn_time + (total + 30) * time_gap:

                        # go back to the staring menu
                        status = "menu"
                        menu = Menu(self.screen)

                    # when a certain time is not passed
                    else:

                        # and if the game over sound hasn't been played
                        if not self.game_over_sound_played:

                            # play the game over sound
                            play_sound("gameover")
                            self.game_over_sound_played = True

                        # empty all the groups to cleat the background
                        self.background_group.empty()
                        self.basic_number_group.empty()
                        self.fast_number_group.empty()
                        self.power_number_group.empty()
                        self.armor_number_group.empty()
                        self.other_number_group.empty()

                        # load the game over image and place it at the right position
                        game_over = StaticSprite()
                        game_over.load("images/game_over.png", 768, 672, 0, 0)
                        game_over.position = 0, 0
                        self.background_group.add(game_over)

                # a special condition is that the player finished the level 35 which is the
                # last level of the game
                elif self.game.level == 35:

                    # after a certain time
                    if ticks > self.spawn_time + (total + 18) * time_gap:

                        # end the scoring board and go back to the starting menu
                        status = "menu"
                        menu = Menu(self.screen)

            # now is the flickering part
            # each change on the screen is called a "appear"
            # each change should only take place if the its appearing order meets the "appear order"
            # appear order is calculated by find how many time gaps were passed
            appear_order = (ticks - self.spawn_time) // time_gap

            # enter the change images process only if the appear order has changed
            # otherwise, the score sound clip may be played for an unexpected anount of time
            if appear_order != self.last_appear_order:

                # record the last appear order in order to detect the change
                self.last_appear_order = appear_order

                # when appear order is still a reasonable number
                if appear_order <= total:

                    # get the detail of the change that needs to make
                    tank_code = self.elimination_list[appear_order-1]

                    # play the score sound clip
                    play_sound("score")

                    # using the example of  "BX" and "B"
                    # "BX" means no basic tanks hit in the previous level,
                    # then print the score and kill number (both 0) directly
                    if tank_code == "BX":
                        points = self.basic_counter * 100

                        self.basic_number_group.empty()
                        print_number(points, "white", 168, 264, self.basic_number_group)
                        print_number(self.basic_counter, "white", 336, 264, self.basic_number_group)

                    # "B" means a hit
                    # if so the number of kills and the score need to be changed
                    # for example from 3, 300 to 4, 400
                    # counter needs to be calculated again in this case
                    elif tank_code == "B":
                        self.basic_counter += 1
                        points = self.basic_counter * 100

                        self.basic_number_group.empty()
                        print_number(points, "white", 168, 264, self.basic_number_group)
                        print_number(self.basic_counter, "white", 336, 264, self.basic_number_group)

                    # same rules apply as above
                    elif tank_code == "FX":
                        points = self.fast_counter * 200

                        self.fast_number_group.empty()
                        print_number(points, "white", 168, 336, self.fast_number_group)
                        print_number(self.fast_counter, "white", 336, 336, self.fast_number_group)

                    elif tank_code == "F":
                        self.fast_counter += 1
                        points = self.fast_counter * 200

                        self.fast_number_group.empty()
                        print_number(points, "white", 168, 336, self.fast_number_group)
                        print_number(self.fast_counter, "white", 336, 336, self.fast_number_group)

                    elif tank_code == "PX":
                        points = self.power_counter * 300

                        self.power_number_group.empty()
                        print_number(points, "white", 168, 408, self.power_number_group)
                        print_number(self.power_counter, "white", 336, 408, self.power_number_group)

                    elif tank_code == "P":
                        self.power_counter += 1
                        points = self.power_counter * 300

                        self.power_number_group.empty()
                        print_number(points, "white", 168, 408, self.power_number_group)
                        print_number(self.power_counter, "white", 336, 408, self.power_number_group)

                    elif tank_code == "AX":
                        points = self.armor_counter * 400

                        self.armor_number_group.empty()
                        print_number(points, "white", 168, 480, self.armor_number_group)
                        print_number(self.armor_counter, "white", 336, 480, self.armor_number_group)

                    elif tank_code == "A":
                        self.armor_counter += 1
                        points = self.armor_counter * 400

                        self.armor_number_group.empty()
                        print_number(points, "white", 168, 480, self.armor_number_group)
                        print_number(self.armor_counter, "white", 336, 480, self.armor_number_group)

                # when the appear order is greater than the length of elimination list
                # a final total number of kills need to be printed
                if appear_order == total + 1:

                    # play the score sound clip
                    play_sound("score")

                    # calculate the overall elimination number
                    total_elimination = self.basic_counter + self.fast_counter + self.power_counter + self.armor_counter

                    # print the total number on the screen
                    print_number(total_elimination, "white", 336, 528, self.other_number_group)

            # update and draw the sprites
            self.update()
            self.draw()

# initialize pygame
pygame.init()

# initialize pygame sound mixer
pygame.mixer.init()

# create a screen with a given size
screen = pygame.display.set_mode((768, 672))

# name the window as "Battle City"
pygame.display.set_caption("Battle City")

# set up the pygame timer
timer = pygame.time.Clock()

# create the Menu object which controls the staring menu of the game
menu = Menu(screen)

# other objects are currently not assigned
level = None
game = None
board = None

# status can be "menu", "level", "game", "board"
# but at the start of the game, the progarm is entering the staring menu atuomatically
status = "menu"

# set up score, live and player tank
score = 0
life = 2
player_1 = PlayerTank(0)

# set up the loop to keep the pygame running
while True:

    # set up fps
    timer.tick(30)

    # ticks is used as a time parameter to prevent the game from refreshing at a high rate
    ticks = pygame.time.get_ticks()

    # release list records the keys being releasing in a loop
    release = []

    # loop through the events in a while loop
    for event in pygame.event.get():

        # quit the game if a QUIT event is detected
        if event.type == QUIT:
            sys.exit()

        # record the keys being releasing to the release list
        if event.type == KEYUP:
            if event.key == pygame.K_SPACE:
                release.append("SPACE")
            elif event.key == pygame.K_s:
                release.append("s")
            elif event.key == pygame.K_w:
                release.append("w")
            elif event.key == pygame.K_RETURN:
                release.append("RETURN")

    # detect the keys being pressed
    keys = pygame.key.get_pressed()

    # quit the game if Esc is pressed
    if keys[K_ESCAPE]:
        sys.exit()

    # run a certain type of status when the game is in one of the four statuses
    if status == "menu":
        menu.run()
    elif status == "level":
        level.run()
    elif status == "game":
        game.run()
    elif status == "board":
        board.run()

    # update the display of the game
    pygame.display.update()
