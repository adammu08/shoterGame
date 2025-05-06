from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina import texture_importer
import time
import random



app = Ursina()
window.title = 'Dungeon Crawler'      # The window title
window.borderless = False            # Show a border
window.fullscreen = True            # Go Fullscreen
window.exit_button.visible = True    # Show the in-game red X that loses the window
window.fps_counter.enabled = True    # Show the FPS (Frames per second) counter

random.seed(0)

ground = Entity(model='plane', collider='box', scale=128, texture='brick.png', texture_scale=(64,64))
ground2 = Entity(model='plane', collider='box', scale=256, texture='brick.png', texture_scale=(128,128))
ground3 = Entity(model='plane', collider='box', scale=128, texture='grass2.png', texture_scale=(128,128))
Enemytest = Entity(model='cube', collider='box', scale=(50,100,1), texture='brick.png', texture_scale=(50,100))#wall floor
Enemytest2 = Entity(model='cube', collider='box', scale=(50,100,1), texture='brick.png', texture_scale=(50,100))
Enemytest3 = Entity(model='cube', collider='box', scale=(5,115,5), texture='brick.png', texture_scale=(5,100))
Enemytest4 = Entity(model='cube', collider='box', scale=(5,115,5), texture='brick.png', texture_scale=(5,100))
Enemytest5 = Entity(model='cube', collider='box', scale=(1,120,100), texture='brick.png', texture_scale=(50,100))#entrey wall
Enemytest6 = Entity(model='cube', collider='box', scale=(100,1,15), texture='brick.png', texture_scale=(100,30))

Enemytest.position=(40,1,25)
Enemytest2.position=(40,1,10)
Enemytest3.position=(64,1,25)
Enemytest4.position=(64,1,10)
Enemytest5.position=(15,1,10)
Enemytest6.position=(64,50,18)
ground2.position=(64,-10,24)
ground3.position=(64,49.999999999,24)
playerspeed = 8
editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.black, origin_y=-.5, speed=playerspeed, collider='box')
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))
gun = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.red, on_cooldown=False)
gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.white, enabled=False)
player_health_ui = HealthBar(value=100, max_value=100, position=(-0.5, 0.45), scale=(0.3, 0.02))
sprint_bar = HealthBar(value=100, max_value=100,color=color.green,position=(-0.5, 0.4), scale=(0.3, 0.02))
sprint_bar.color=color.green
player.hp = 100
player.position=(50,100,17)

music_files = ['Apple_Groove.wav', 'Chill2.wav', 'winter.wav']
current_index = 0
music = Audio(music_files[current_index], loop=False, autoplay=True)
def play_next_song():
    global current_index
    current_index = (current_index + 1) % len(music_files) 
    music

def check_music_end():
    if not music.playing:
        play_next_song()
    else:
        invoke(check_music_end, delay=1)


def take_damage(amount):
    player.hp -= amount
    player_health_ui.value = player.hp
    if player.hp <= 0:
        print('the game has ended')


        
shootables_parent = Entity()
mouse.traverse_target = shootables_parent
last_heal_time = 0
last_punch_time=0
last_sprint_time=0
running_time=0
def update():
    global last_heal_time
    global last_punch_time
    global last_sprint_time
    global running_time
    if held_keys['left mouse']:
        shoot()

    if held_keys['v'] and time.time() - last_punch_time > 2:
        hit()
        last_punch_time = time.time()

    if held_keys['h'] and time.time() - last_heal_time > 1.5:
        heal()
        last_heal_time = time.time()

    if held_keys['shift'] and sprint_bar.value > 0:
        sprint()
        if time.time() - running_time > .1:
            sprint_bar.value -= 1
            running_time = time.time()
    
    if time.time() - last_sprint_time > 5:
        sprint_bar.value += 5
        last_sprint_time = time.time()

    if time.time() - running_time > .1:
        player.speed = 8
        running_time = time.time()
        


def sprint():
    if sprint_bar.value > 0:
        player.speed = 12
    elif sprint_bar.value == 0:
        player.speed = 5
    else:
        player.speed = 8
    
    

def shoot():
    if not gun.on_cooldown:
        gun.on_cooldown = True
        gun.muzzle_flash.enabled=True
        from ursina.prefabs.ursfx import ursfx
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.8, wave='noise', pitch=random.uniform(-13,-12), pitch_change=-12, speed=3.0)
        invoke(gun.muzzle_flash.disable, delay=.05)
        invoke(setattr, gun, 'on_cooldown', False, delay=3.5)
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            distance = (player.position - mouse.hovered_entity.position).length()
            if distance <= 25:
                mouse.hovered_entity.hp -= 10
                mouse.hovered_entity.blink(color.red)
def hit():
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            distance = (player.position - mouse.hovered_entity.position).length()
            if distance <= 5:
                mouse.hovered_entity.hp -= 2.5
                mouse.hovered_entity.blink(color.red)
def heal():
    if player.hp < 100:
        if player_health_ui < 100:
                player_health_ui.value = 100
                player.hp = 100
                
class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model='cube', scale_y=1, origin_y=-.5, color=color.green,texture='slime.png', collider='box', **kwargs)
        self.texture = load_texture('slime.png')
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5,.1,.1))
        self.max_hp = 25
        self.hp = self.max_hp
        self.last_attack_time = 0
    def attack_player(self):
        if time.time() - self.last_attack_time > 1.5:
            take_damage(5)  
            self.last_attack_time = time.time()

    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 15:
            return
        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)


        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
        
        if hit_info.entity == player:
            
            if dist < 2.5:
                self.attack_player() 
            else:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1

# Enemy()
enemies = [Enemy(x=x*4) for x in range(4)]

class zombie(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model='cube',Texture='zombite.png',color=color.rgb(-1,1,-1), scale_y=2, origin_y=-.5,collider='box', **kwargs)
        self.texture = load_texture('zombite.png')
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5,.1,.1))
        self.max_hp = 50
        self.hp = self.max_hp
        self.last_attack_time = 0
    def attack_player(self):
        if time.time() - self.last_attack_time > 1.5: 
            take_damage(15) 
            if time.time() - self.last_attack_time > 5: 
                take_damage(5)
            self.last_attack_time = time.time()  

    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 15:
            return
        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)


        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 35, ignore=(self,))
        
        if hit_info.entity == player:
            
            if dist < 4.5:
                self.attack_player() 
            else:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1

# zombie
zombie = [zombie(x=x*10) for x in range(4)]

def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

slime=[Enemy(x=x*1)for x in range(1)]

app.run()