from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina import texture_importer
from ursina.lights import AmbientLight
import time
import random

def get_enemy_count():
    return sum(isinstance(e, (Enemy, zombie, boneman, boss1)) for e in shootables_parent.children)
#how to define the game
app = Ursina()
window.title = 'Dungeon Crawler'      # The window title
window.borderless = False            # Show a border
window.fullscreen = True            # Go Fullscreen
window.exit_button.visible = False    # Show the in-game red X that loses the window
window.fps_counter.enabled = True   # Show the FPS (Frames per second) counter
Sky()
random.seed(0)
#all of the world genration
AmbientLight(color=color.rgba(100, 100, 100, 255))
scene.fog_density = 0.1
scene.fog_color = color.gray
ground = Entity(model='plane', collider='mesh', scale=128, texture='brick.png', texture_scale=(64,64),shadows=False)
ground3 = Entity(model='plane', collider='mesh', scale=384, texture='grass3.png', texture_scale=(16,16),shadows=False)
Enemytest = Entity(model='cube', collider='mesh', scale=(50,2,1), texture='brick.png', texture_scale=(50,2),shadows=False)#wall floor
Enemytest2 = Entity(model='cube', collider='mesh', scale=(50,2,1), texture='brick.png', texture_scale=(50,2),shadows=False)
Enemytest3 = Entity(model='cube', collider='mesh', scale=(5,15,5), texture='brick.png', texture_scale=(5,100),shadows=False)#tower
Enemytest4 = Entity(model='cube', collider='mesh', scale=(5,15,5), texture='brick.png', texture_scale=(5,100),shadows=False)#tower
Enemytest5 = Entity(model='cube', collider='mesh', scale=(1,25,100), texture='brick.png', texture_scale=(100,25),shadows=False)#entrey wall
Enemytest6 = Entity(model='cube', collider='mesh', scale=(100,1,15), texture='brick.png', texture_scale=(100,30),shadows=False)
entry = Entity(model='cube', collider='mesh', scale=(1,10,15), texture='door4.png', texture_scale=(1,1),shadows=False)
Enemytest.position=(40,50,25)
Enemytest2.position=(40,50,10)
Enemytest3.position=(64,50,25)
Enemytest4.position=(64,50,10)
Enemytest5.position=(15,50,10)
Enemytest6.position=(64,50,18)
entry.position=(15.01,55.5,17.4)
ground3.position=(64,49.999999999,24)
#how the player things spawn with some text
playerspeed = 8
player_coords_text = Text(position=(-0.7,-.45), scale=1, color=color.white)
popup_text = Text(text='Welcome to Dungeon Crawler!', scale=2, origin=(0,0), color=color.white)
editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController(model='cube', z=-10, color=color.black, origin_y=-.5, speed=playerspeed, collider='box')
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))
gun = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.red, on_cooldown=False,shadows=False)
gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.white, enabled=False,shadows=False)
player_health_ui = HealthBar(value=100, max_value=100, position=(-0.5, 0.45), scale=(0.3, 0.02),shadows=False)
sprint_bar = HealthBar(value=100, max_value=100,color=color.green,position=(-0.5, 0.4), scale=(0.3, 0.02),shadows=False)
sprint_bar.color=color.green
player.hp = 100
player.position=(50,100,17)
spawn_points = [
    Vec3(10, 0, 10),
    Vec3(20, 0, 20),
    Vec3(30, 0, 15),
    Vec3(40, 0, 25)
]


def kill_all_enemies():
    for e in shootables_parent.children:
        if isinstance(e, (Enemy, zombie, boneman, boss1)):
            destroy(e)
    

def distance_xz(pos1, pos2):
    return ((pos1.x - pos2.x) ** 2 + (pos1.z - pos2.z) ** 2) ** 0.5


def spawn_enemy():
    Enemy(position=(35,50,35))
def spawn_zombie():
    zombie(position=(35,50,30))
def spawn_boneman():
    boneman(position=(35,50,40))
def spawn_boss():
    boss1(position=(35,50,45))
#music still need to fix this
music_files = ['music_for_a_game_im_working_on.wav','Apple_Groove.wav', 'Chill2.wav', 'winter.wav']
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


def take_damage(amount):# how the player takes damage and how the dead room works
    player.hp -= amount
    player_health_ui.value = player.hp
    if player.hp <= 0:
        player.position=(200,7,200)
        popup_dead = Text(text='GAME OVER', scale=10, origin=(0,0), color=color.red)
        invoke(destroy, popup_dead, delay=50)
        deadroom = Entity(model='plane', collider='box', scale=20, texture='grass3.png', texture_scale=(10,10))
        deadroomwall1 = Entity(model='cube', collider='box', scale=(1,19,20) , texture='grass3.png', texture_scale=(10,10),shadows=False)
        deadroomwall2 = Entity(model='cube', collider='box', scale=(1,19,20), texture='grass3.png', texture_scale=(10,10),shadows=False)
        deadroomwall3 = Entity(model='cube', collider='box', scale=(20,19,1), texture='grass3.png', texture_scale=(10,10),shadows=False)
        deadroomwall4 = Entity(model='cube', collider='box', scale=(20,19,1), texture='grass3.png', texture_scale=(10,10),shadows=False)
        deadroomwall5 = Entity(model='cube', collider='box', scale=(20,1,20), texture='grass3.png', texture_scale=(10,10),shadows=False)
        deadroom.position=(200,5,200)
        deadroomwall1.position=(210,5,200)
        deadroomwall2.position=(195,5,200)
        deadroomwall3.position=(200,5,195)
        deadroomwall4.position=(200,5,210)
        deadroomwall5.position=(200,14,200)
        
shootables_parent = Entity()
mouse.traverse_target = shootables_parent
last_heal_time = 0
last_punch_time=0
last_sprint_time=0
running_time=0
win = True
def update(): # how the key binds work
    enemy_count_text.text = f"Enemies: {get_enemy_count()}"
    player_coords_text.text = f"Player Coords: X={int(player.x)} Y={int(player.y)} Z={int(player.z)}"
    invoke(destroy, popup_text, delay=5)
    global last_heal_time
    global last_punch_time
    global last_sprint_time
    global running_time
    
    if get_enemy_count() == 0 and True:
        ye = Text(text='you win', scale=5, origin=(0,0), color=color.yellow)
        invoke(destroy, ye, delay=10)
        False
    if held_keys['left mouse']:
        shoot()

    if held_keys['v'] and time.time() - last_punch_time > 2:
        hit(5)
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
    if held_keys['0']:
        spawn_zombie()
        spawn_enemy()
        spawn_boneman()
        spawn_boss()
    if held_keys['9']:
        hit(100)
    if held_keys['8']:
        kill_all_enemies()
   
    if  held_keys['f']:
            spawn_point = dungeon.get_spawn_point()
            player.position = spawn_point
def sprint(): #how the player runs
    if sprint_bar.value > 0:
        player.speed = 12
    elif sprint_bar.value == 0:
        player.speed = 5
    else:
        player.speed = 8
    

def shoot():#how to use the crossbow
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
                mouse.hovered_entity.hp -= 25
                mouse.hovered_entity.blink(color.red)
def hit(amount):#the punch
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            distance = (player.position - mouse.hovered_entity.position).length()
            if distance <= 5:
                mouse.hovered_entity.hp -= amount
                mouse.hovered_entity.blink(color.red)
def heal():#how the player heals
    if player.hp < 100:
        if player_health_ui < 100:
                player_health_ui.value = 100
                player.hp = 100
                
class Enemy(Entity):#class for how to spawn the slimes
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model='cube',speed=10,scale_y=1, origin_y=-.5, color=color.green,texture='slime.png', collider='box', **kwargs,shadows=False)
        self.texture = load_texture('slime.png')
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5,.1,.1),shadows=False)
        self.max_hp = 25
        self.hp = self.max_hp
        self.last_attack_time = 0
    def attack_player(self):
        if time.time() - self.last_attack_time > 1.5:
            take_damage(5)  
            self.last_attack_time = time.time()

    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 20:  # Skip updates for enemies far from the player
            return
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


class zombie(Entity): #class for zombie
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model='cube',Texture='zombite.png',color=color.rgb(-1,1,-1), scale_y=2, origin_y=-.5,collider='box', **kwargs,shadows=False)
        self.texture = load_texture('zombite.png')
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5,.1,.1),shadows=False)
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
        if dist > 20:  # Skip updates for enemies far from the player
            return
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

class boneman(Entity): #class for skeliton
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model='cube',color=color.gray, scale_y=2, origin_y=-.5,collider='box', **kwargs,shadows=False)
        
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5,.1,.1),shadows=False)
        self.max_hp = 75
        self.hp = self.max_hp
        self.last_attack_time = 0
    def attack_player(self):
        if time.time() - self.last_attack_time > 3: 
            take_damage(15) 
            self.last_attack_time = time.time()  

    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 20:  # Skip updates for enemies far from the player
            return
        dist = distance_xz(player.position, self.position)
        if dist > 15:
            return
        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)


        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 35, ignore=(self,))
        
        if hit_info.entity == player:
            dist = distance_xz(player.position, self.position)
            if dist < 15:
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


# skeltion
    
class boss1(Entity):#class for how to spawn the slimes
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model='cube',speed=5,scale=(4,4,4), origin_y=-.5, color=color.green,texture='slime.png', collider='box', **kwargs,shadows=False)
        self.texture = load_texture('slime.png')
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5,.1,.1),shadows=False)
        self.max_hp = 500
        self.hp = self.max_hp
        self.last_attack_time = 0
    def attack_player(self):
        if time.time() - self.last_attack_time > 1.5:
            take_damage(5)  
            self.last_attack_time = time.time()

    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 20:  # Skip updates for enemies far from the player
                return
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
                self.position += self.forward * time.dt * 2 #what the speed is

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


#how to controll enemys spawn
slime = [Enemy(position=spawn_point) for spawn_point in spawn_points]

zombie_new = [zombie(position=spawn_point) for spawn_point in spawn_points]

new_bone = [boneman(position=spawn_point) for spawn_point in spawn_points]

new_boss = [boss1(position=spawn_point) for spawn_point in spawn_points]

# Dungeon Settings

width, height = 100, 20  # Overall dungeon size
tile_size = 5


class DungeonGenerator(Entity):
    def __init__(self, width=100, height=20, tile_size=5, num_rooms=50):
        super().__init__()
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.dungeon_map = [['wall' for _ in range(self.width)] for _ in range(self.height)]
        self.rooms = []
        self.boss_room = None

        self.generate_rooms(num_rooms)
        self.generate_corridors()
        self.generate_boss_room()  # Add the boss room
        self.build_dungeon()

    def generate_rooms(self, num_rooms):
        # Generate random rooms and store their centers.
        for _ in range(num_rooms):
            w, h = random.randint(3, 6), random.randint(3, 6)
            x, y = random.randint(1, self.width - w - 1), random.randint(1, self.height - h - 1)

            for i in range(h):
                for j in range(w):
                    self.dungeon_map[y + i][x + j] = 'floor'

            self.rooms.append((x + w // 2, y + h // 2))  # Store room center coordinates

    def generate_corridors(self):
        # Connect rooms using Bresenham's line algorithm for smooth paths.
        def bresenham_line(x1, y1, x2, y2):
            points = []
            dx, dy = abs(x2 - x1), abs(y2 - y1)
            sx, sy = (1 if x2 > x1 else -1), (1 if y2 > y1 else -1)
            err = dx - dy

            while x1 != x2 or y1 != y2:
                points.append((x1, y1))
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy
            points.append((x2, y2))  # Include the endpoint
            return points

        for i in range(len(self.rooms) - 1):
            x1, y1 = self.rooms[i]    # Start room center
            x2, y2 = self.rooms[i+1]  # End room center

            # Generate horizontal and vertical corridors
            corridor_points = bresenham_line(x1, y1, x2, y1) + bresenham_line(x2, y1, x2, y2)

            # Clear walls along the corridor path
            for x, y in corridor_points:
                if 0 <= x < self.width and 0 <= y < self.height:  # Ensure within bounds
                    self.dungeon_map[y][x] = 'floor'

    def generate_boss_room(self):
        # Randomly select a room to be the boss room.
        if self.rooms:
            boss_room_index = random.randint(0, len(self.rooms) - 1)
            self.boss_room = self.rooms[boss_room_index]
            x, y = self.boss_room
            w, h = 5, 5
            # Create a larger room for the boss
            for i in range(h):
                for j in range(w):
                    if 0 <= x + j < self.width and 0 <= y + i < self.height:
                        self.dungeon_map[y + i][x + j] = 'boss'
            # Mark the boss room with a different tile type
            self.dungeon_map[y + h // 2][x + w // 2] = 'boss'
            # Add a boss spawn point
            self.dungeon_map[y + h // 2][x + w // 2] = 'boss spawn'
            # Add a boss spawn point
            self.boss_room = (x + w // 2, y + h // 2)
    

    def spawn_enemies_in_rooms(self, num_enemies):
        for _ in range(num_enemies):
            if not self.rooms:
             return  # No rooms available

            # Randomly select a room
            room_center = random.choice(self.rooms)
            room_x, room_y = room_center

            # Randomize position within the room
            room_width, room_height = random.randint(3, 6), random.randint(3, 6)  # Adjust room size as needed
            random_x = random.randint(room_x - room_width // 2, room_x + room_width // 2)
            random_y = random.randint(room_y - room_height // 2, room_y + room_height // 2)

            # Ensure the position is within bounds and on a floor tile
            if 0 <= random_x < self.width and 0 <= random_y < self.height and self.dungeon_map[random_y][random_x] == 'floor':
                # Convert to 3D position
                spawn_position = (random_x * self.tile_size, 2.5, random_y * self.tile_size)  # Set Y to 0 (floor level)

                # Spawn an enemy (randomly choose enemy type)
                enemy_type = random.choice([Enemy, zombie, boneman])
                enemy_type(position=spawn_position)

    def add_roof(self):
   
        roof_height = self.tile_size * 2  # Adjust height to be above the walls
        roof = Entity(
            model='cube',
            texture='brick',  # Replace with your roof texture
            texture_scale=(self.width * self.tile_size, self.height * self.tile_size),
            scale=(self.width * self.tile_size, self.height * self.tile_size, 1),
            position=(self.width * self.tile_size / 2, 8, self.height * self.tile_size / 2),
            rotation=(90, 0, 0),  # Rotate to make it horizontal
            collider=None,  # No collision needed for the roof
            shadows=False
            )

    def build_dungeon(self):
        # Convert dungeon grid to 3D entities in Ursina.
        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.dungeon_map[y][x]
                position = (x * self.tile_size, 0 if tile_type in ['floor', 'boss'] else self.tile_size, y * self.tile_size)
                texture = 'brick' if tile_type == 'floor' else 'brick' if tile_type == 'wall' else 'boss room text'

                Entity(model='cube', texture=texture, texture_scale=(5, 5), collider='mesh', scale=self.tile_size, position=position,shadows=False)

    def get_boss_room_center(self):
        # Return the 3D position of the boss room's center
        if self.boss_room:
            x, y = self.boss_room
            return (x * self.tile_size, self.tile_size, y * self.tile_size)
        return None
    def get_spawn_point(self):
        # Return the 3D position of the first room's center
        if self.rooms:
            x, y = self.rooms[0]  # Use the first room as the spawn point
            return (x * self.tile_size, self.tile_size, y * self.tile_size)
        return (0, self.tile_size, 0)  # Default spawn point 
    
kill_all_enemies()
dungeon = DungeonGenerator()
dungeon.generate_boss_room()
dungeon.spawn_enemies_in_rooms(65)  # Spawn enemies in the dungeon

dungeon.add_roof()
boss_spawn_point = dungeon.get_boss_room_center()
if boss_spawn_point:
    boss = boss1(position=(boss_spawn_point[0], 2, boss_spawn_point[2]))
#how to run the game

enemy_count_text = Text(position=(-0.7, 0.4), scale=1, color=color.yellow)
get_enemy_count()
    
app.run()
