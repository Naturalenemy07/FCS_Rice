# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
rock_total = 0
started = False
DIMENSIONS = 2
THRUST_SCALER = 0.3
SHIP_IMAGE_WIDTH = 90
SHIP_IMAGE_HEIGHT_FROM_CENTER = 45
FRICTION_COEFFICIENT = 0.02
SHIP_ANG_VEL_COEFFICIENT = 0.085
ROCK_MIN_VEL = -1
ROCK_MAX_VEL = 1
ROCK_ANG_VEL_COEFFICIENT = 0.1
ROCK_MIN_ANG_VEL = -1
ROCK_MAX_ANG_VEL = 1
ROCK_MAX = 12
MISSILE_SCALAR = 5
SPRITE_AGE_INCREMENT = 0.8
ROCK_SHIP_DIST = 90

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def group_collide(group, other_object):
    global rock_group, rock_total, score
    ship_interaction = 0
    missile_interaction = 0
    
    # create a iterable set
    iter_group = set([])
    for object in group:
        if object.collide(other_object):
            iter_group.add(object)
            if other_object is my_ship:
                ship_interaction = 1
            else:
                missile_interaction = 1

    if ship_interaction == 1:
        for object in iter_group:
            rock_group.remove(object)
            rock_total -= 1
        return True
    
    if missile_interaction == 1:
        for object in iter_group:
            rock_group.remove(object)
            rock_total -= 1
            score += 1
        return False

def group_group_collide(group1, group2):
    group1_copy = group1.copy()
      
    for item in group1_copy:
        group_collide(group2, item)   
    
def process_sprite_group(canvas, set_original):
    # make a copy of set to avoid iterating over a set we are modifying
    set_copy = set()
    
    for item in set_original:
        if item.update():
            set_copy.add(item)
    for sprite in set_copy:
        set_original.remove(sprite)
    for sprite in set_original:
        sprite.update()
        sprite.draw(canvas)

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def keydown(key):
    # Spaceship control
    if started == True:
        lr_keys = {'left': -1 * SHIP_ANG_VEL_COEFFICIENT, 'right': SHIP_ANG_VEL_COEFFICIENT}
        for k in lr_keys:
            if key == simplegui.KEY_MAP[k]:
                my_ship.angle_vel = lr_keys[k]
        if key == simplegui.KEY_MAP['up']:
            my_ship.thrusters(True)

        # Missle firing
        if key == simplegui.KEY_MAP['space']:
            my_ship.shoot()
    
    
def keyup(key):
    keys = {'left': 0, 'right': 0}
    for k in keys:
        if key == simplegui.KEY_MAP[k]:
            my_ship.angle_vel = keys[k]
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrusters(False)
        
# mouse handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.rewind() 
        soundtrack.play()
        lives = 3
        score = 0 
            
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.fwd_vector = [0,0]
        
    def draw(self,canvas):
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        elif self.thrust == True:
            #Tiled image: thrusters on is image next to it so add image width to get to next image
            image_thrusters_on_center = [self.image_center[0] + SHIP_IMAGE_WIDTH, self.image_center[1]]
            canvas.draw_image(self.image, image_thrusters_on_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # compute angular velocity for rotating ship
        for i in range(DIMENSIONS):
            self.pos[i] += self.vel[i]
        self.angle += self.angle_vel
        
        # compute forward vector of length 1
        self.fwd_vector = angle_to_vector(self.angle)
        
        # thrust in the direction of fwd_vector
        if self.thrust:
            for i in range(DIMENSIONS):
                # Multiply the fwd_vector by a THRUST_SCALER to prevent the ship from accelerating so fast it can't be controlled
                self.vel[i] += THRUST_SCALER * self.fwd_vector[i]
                # Subtract the friction component after thrust has been calculated (requires to be two lines because the operation is different
                self.vel[i] *= (1 - FRICTION_COEFFICIENT)
        elif not self.thrust:
            for i in range(DIMENSIONS):
                # Subtract the friction component from velocity
                self.vel[i] *= (1 - FRICTION_COEFFICIENT)
            
                
        # set boundary conditions for the ship
        if self.pos[0] > WIDTH or self.pos[0] < 0:
            self.pos[0] %= WIDTH
        if self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.pos[1] %= HEIGHT
            
    def thrusters(self, thrust_bool):
        self.thrust = thrust_bool

        # play sound when thrusters are turned on and rewind when not turned on
        if self.thrust:
            ship_thrust_sound.play()
        elif not self.thrust:
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global a_missile, missle_group
        ship_tip = [0,0]
        
        # calculate the velocity of missile, multiply by a scalar 
        mis_vel = [0,0]
        for i in range(DIMENSIONS):
            mis_vel[i] = self.vel[i] + MISSILE_SCALAR * self.fwd_vector[i]
            
            ship_tip[i] = self.pos[i] + self.fwd_vector[i]*SHIP_IMAGE_HEIGHT_FROM_CENTER
            
        # make the missile in shoot function    
        missile_group.add(Sprite(ship_tip, mis_vel, 0, 0, missile_image, missile_info, missile_sound))
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def collide(self, other_object):
        # return true if collision
        # return false if no collision
        
        # get the distance between self and other_object
        if dist(self.pos, other_object.pos) <= self.radius + other_object.radius:
            return True
        else:
            return False
        
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        #position of sprite in 2 dimensions, change angle
        for i in range(DIMENSIONS):
            self.pos[i] += self.vel[i]
        self.angle += self.angle_vel
        
        # set boundary conditions for the ship
        if self.pos[0] > WIDTH or self.pos[0] < 0:
            self.pos[0] %= WIDTH
        if self.pos[1] > HEIGHT or self.pos[1] < 0:
            self.pos[1] %= HEIGHT
        
        # increment sprite age
        self.age += SPRITE_AGE_INCREMENT
        if self.age < self.lifespan:
            return False      
        else:
            return True
            
# draws images          
def draw(canvas):
    global time, missile_group, my_ship, rock_group, lives, score, started, rock_total
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    for rock in rock_group:
        rock.draw(canvas)
    for missile in missile_group:
        missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    for rock in rock_group:
        rock.update()
    for missile in missile_group:
        missile.update()
    #print len(rock_group)
    
    # collide
    if group_collide(rock_group, my_ship):
        lives -= 1
        
    group_group_collide(missile_group, rock_group)
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
    #call rock group and missile update
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    
    # draw the user interface
    canvas.draw_text('Lives: ' + str(lives), [50, 50], 40, 'Fuchsia')
    canvas.draw_text('Score: ' + str(score), [600, 50], 40, 'Fuchsia')
    
    if lives == 0:
        started = False
        soundtrack.pause()
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        rock_group = set([])
        rock_total = 0
        missile_group = set([])
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, rock_total
    
    # randomly choose a negative or positive value (used for ang_vel)
    pos_neg = [-1, 1]
    rand_pos_neg = random.choice(pos_neg)
    
    #random values used for spawning a new rock
    rand_vel = [random.randrange(ROCK_MIN_VEL, ROCK_MAX_VEL), random.randrange(ROCK_MIN_VEL, ROCK_MAX_VEL)]
    rand_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rand_ang_vel = random.random() * ROCK_ANG_VEL_COEFFICIENT * rand_pos_neg
    
    #spawn rocks in rock group set
    if started == True:
        if dist(rand_pos, my_ship.pos) > ROCK_SHIP_DIST:
            if rock_total < ROCK_MAX:
                rock_group.add(Sprite(rand_pos, rand_vel, 0, rand_ang_vel, asteroid_image, asteroid_info))
                rock_total += 1
            
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sets
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
