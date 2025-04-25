from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
import time
app = Ursina()
window.title = 'Dungeon Crawler'      # The window title
window.borderless = False            # Show a border
window.fullscreen = False            # Go Fullscreen
window.exit_button.visible = True    # Show the in-game red X that loses the window
window.fps_counter.enabled = True    # Show the FPS (Frames per second) counter


random.seed(0)

ground = Entity(model='plane', collider='box', scale=128, texture='white_cube', texture_scale=(64,64))

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.black, origin_y=-.5, speed=8, collider='box')
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))
gun = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.red, on_cooldown=False)
gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.white, enabled=False)
player_health_ui = HealthBar(value=100, max_value=100, position=(-0.5, 0.45), scale=(0.3, 0.02))
healing_tester = Entity(model='cube',texture='helingtemp.png', position=(10,.5,10), color=color.white, scale=(1))
player.hp = 100  # Initial health

def take_damage(amount):
    player.hp -= amount
    player_health_ui.value = player.hp
    if player.hp <= 0:
        print()
shootables_parent = Entity()
mouse.traverse_target = shootables_parent

def update():
    if held_keys['left mouse']:
        shoot()

def shoot():
    if not gun.on_cooldown:
        gun.on_cooldown = True
        gun.muzzle_flash.enabled=True
        from ursina.prefabs.ursfx import ursfx
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise', pitch=random.uniform(-13,-12), pitch_change=-12, speed=3.0)
        invoke(gun.muzzle_flash.disable, delay=.05)
        invoke(setattr, gun, 'on_cooldown', False, delay=.05)
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            mouse.hovered_entity.hp -= 10
            mouse.hovered_entity.blink(color.red)
            




class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model='cube', scale_y=1, origin_y=-.5, color=color.green, collider='box', **kwargs)
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
            
            if dist < 2:
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

class zombit(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model='cube',Texture='zombite.png' , scale_y=2, origin_y=-.5, color=color.green,collider='box', **kwargs)
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.green, world_scale=(1.5,.1,.1))
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
            
            if dist < 2:
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

# zombit
zombit = [zombit(x=x*10) for x in range(4)]

def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)

app.run()