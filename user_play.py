from game_lib.sprites import Mario, Mushroom, Fireball, ObstacleGroup, MarioGroup
import pygame

resolution = (800, 400)

caption = "Mario! :D"

background_image = "images/background.png"
mario_img_loc = "images/super-mario-png-paper-mario-icon-256.png"
mushroom_img_loc = "images/cogumelo-do-mario-png-1.png"
ducking_img_loc = "images/mario_crouh.png"
fireball_img_loc = "images/fireball.png"

jump_vel = 40
gravity = 7
frame_rate = 30
bg = pygame.image.load(background_image)

RELEASED = True
WAITING = False


def get_key_event(game_over=False):
    _state = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _state = "quit"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                _state = "jump"
            elif event.key == pygame.K_DOWN:
                _state = "duck"
            elif event.key == pygame.K_LEFT:
                _state = "bw"
            elif event.key == pygame.K_RIGHT:
                _state = "fw"
        elif event.type == pygame.KEYUP:
            _state = "reset"
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                _state = "halt"
            if game_over:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    _state = "restart"
                elif event.key == pygame.K_ESCAPE:
                    _state = "quit"
    return _state


def game_over_screen(screen):
    _font = pygame.font.SysFont('Purisa', 50)
    textsurface = _font.render('Game Over', False, (0, 0, 0))
    screen.blit(textsurface, (screen_w // 2 - textsurface.get_width() // 2,
                              screen_h // 2 - textsurface.get_height() // 2))
    _font2 = pygame.font.SysFont('Purisa', 20)
    textsurface2 = _font2.render('Press Enter to restart. ESC to quit', True, (0, 0, 0))
    screen.blit(textsurface2, (screen_w // 2 - textsurface2.get_width() // 2,
                               screen_h // 2 + 30))


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    # initialize canvas
    screen = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    pygame.display.set_caption(caption)

    background = bg.convert()
    screen.blit(background, (0, 0))

    screen_w, screen_h = resolution
    wlim, hlim = screen_w - 32, screen_h - 70

    mario_properties = {
        'image': mario_img_loc,
        'resize_to': (32, 32),
        'ducked_image': ducking_img_loc,
        'ducked_resize_to': (28, 28),
        'X': wlim * .1,
        'Y': hlim,
        'resolution': resolution,
        'horizontal_step': 10,
        'gravity': gravity,
        'jump_vel': jump_vel,
        'gene': None
    }

    mario = Mario(**mario_properties)

    mushroom1 = Mushroom(image=mushroom_img_loc, resize_to=(32, 32), Y=hlim, resolution=resolution)
    mushroom2 = Mushroom(image=mushroom_img_loc, resize_to=(32, 32), Y=hlim, resolution=resolution)
    fireball1 = Fireball(image=fireball_img_loc, resize_to=(32, 32), Y=hlim - 28, resolution=resolution)
    fireball2 = Fireball(image=fireball_img_loc, resize_to=(32, 32), Y=hlim - 28, resolution=resolution)

    mario_group = MarioGroup()
    mario_group.add(mario)
    obstacle_group = ObstacleGroup(release_count=2, release_dist=wlim // 2)
    obstacles = [mushroom1, mushroom2, fireball1, fireball2]
    obstacle_group.add(obstacles)

    game_over = False
    quited = False
    t0 = t1 = clock.get_time()

    state = prev_state = ""
    while True:
        state = get_key_event(game_over)
        if state == "quit":
            break
        if state is None:
            state = prev_state
        else:
            prev_state = state

        if not game_over:
            mario_group.update(state)
            obstacle_group.update()

            for obstacle in obstacles:
                if mario.rect.colliderect(obstacle.rect):
                    game_over = True
                    break

            screen.blit(background, (0, 0))

            mario_group.draw(screen)
            obstacle_group.draw(screen)

        else:
            if state == "restart":
                mario_group.reset_pos()
                obstacle_group.reset_pos()
                game_over = False
            else:
                game_over_screen(screen)

        pygame.display.update()
        clock.tick(frame_rate)

    print("Game Over")
    # place("player", player.loc)
    # play()
