import pygame


class GamePlay:
    def __init__(self, players, obstacles, resolution, background,
                 caption="Mario!", frame_rate = 30):
        self.players = players
        self.obstacles = obstacles
        self.frame_rate = frame_rate

        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(caption)

        self.screen_w, self.screen_h = resolution
        # self.wlim, self.hlim = self.screen_w - 32, self.screen_h - 70

        bg = pygame.image.load(background)
        self.background = bg.convert()

        self.screen.blit(self.background, (0, 0))

    def play(self):
        pygame.init()
        pygame.font.init()

        for player in self.players:
            print(player)

        _state = None
        while True:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _state = "quit"
            if _state == "quit":
                break

            pygame.display.update()
            self.clock.tick(self.frame_rate)

        # self.game_over_screen()

    def game_over_screen(self):
        _font = pygame.font.SysFont('Purisa', 50)
        text_surface = _font.render('Game Over', False, (0, 0, 0))
        self.screen.blit(text_surface, (self.screen_w // 2 - text_surface.get_width() // 2,
                                       self.screen_h // 2 - text_surface.get_height() // 2))
        _font2 = pygame.font.SysFont('Purisa', 20)
        text_surface_2 = _font2.render('Press Enter to restart. ESC to quit', True, (0, 0, 0))
        self.screen.blit(text_surface_2, (self.screen_w // 2 - text_surface_2.get_width() // 2,
                                        self.screen_h // 2 + 30))
