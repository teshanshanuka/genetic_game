from game_lib.canvas import GamePlay
from game_lib.sprites import Mushroom, Fireball

NO_PLAYERS = 5
BACKPROPEGATION_UPDATE_COUNT = 5
MAX_POINTS = 100

resolution = (800, 400)
caption = "Mario! :D"

background_image = "images/background.png"
mario_img = "images/super-mario-png-paper-mario-icon-256.png"
mushroom_img = "images/cogumelo-do-mario-png-1.png"
ducking_img = "images/mario_crouh.png"
fireball_img = "images/fireball.png"

jump_vel = 40
gravity = 7
frame_rate = 30
#
screen_w, screen_h = resolution
wlim, hlim = screen_w - 32, screen_h - 70

mario_properties = {
    'image': mario_img,
    'resize_to': (32, 32),
    'ducked_image': ducking_img,
    'ducked_resize_to': (28, 28),
    'X': wlim * .1,
    'Y': hlim,
    'resolution': resolution,
    'horizontal_step': 10,
    'gravity': gravity,
    'max_fail_count': BACKPROPEGATION_UPDATE_COUNT,
    'jump_vel': jump_vel,
    'gene': None
}

mushroom_properties = {
    'image': mushroom_img,
    'resize_to': (32, 32),
    'Y': hlim,
    'resolution': resolution
}

fireball_properties = {
    'image': fireball_img,
    'resize_to': (32, 32),
    'Y': hlim - 28,
    'resolution': resolution
}

if __name__ == "__main__":
    obstacles = [Mushroom(**mushroom_properties), Mushroom(**mushroom_properties),
                 Fireball(**fireball_properties), Fireball(**fireball_properties)]

    game = GamePlay(NO_PLAYERS, mario_properties, obstacles, resolution, MAX_POINTS,
                    background_image, frame_rate=frame_rate)
    game.play()

