from game_lib.sprites import *


class GamePlay:
    def __init__(self, no_players, mario_properties, obstacles: List[Union[Mushroom, Fireball]], resolution, max_score,
                 background, frame_rate=30, caption="Mario!"):
        self.obstacles = obstacles
        self.frame_rate = frame_rate
        self.max_score = max_score
        self.no_players = no_players

        self.screen = pygame.display.set_mode(resolution)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(caption)

        self.screen_w, self.screen_h = resolution
        wlim, hlim = self.screen_w - 32, self.screen_h - 70

        bg = pygame.image.load(background)
        self.background = bg.convert()

        self.screen.blit(self.background, (0, 0))

        self.players = []
        self.mario_group = MarioGroup()
        for _ in range(no_players):
            mario_properties['gene'] = self.get_init_gene()
            player = Mario(**mario_properties)
            self.players.append(player)
            self.mario_group.add(player)

        self.obstacle_group = ObstacleGroup(release_count=2, release_dist=wlim // 2)
        for obstacle in obstacles:
            self.obstacle_group.add(obstacle)

    def play(self):
        pygame.init()
        pygame.font.init()

        round = 1

        _state = None
        while True:
            self.mario_group.update(self.obstacles)
            self.obstacle_group.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    _state = "quit"
            if _state == "quit":
                break

            for obstacle in self.obstacles:
                if not obstacle.released:
                    continue
                for player in self.players:
                    if player.rect.colliderect(obstacle.rect) or player.score >= self.max_score:
                        if player.score > 40:
                            player.game_over = True

            if all(player.finished for player in self.players):
                round += 1
                print("Round", round)
                self.respawn_players()

            self.screen.blit(self.background, (0, 0))
            self.mario_group.draw(self.screen)
            self.obstacle_group.draw(self.screen)

            pygame.display.update()
            self.clock.tick(self.frame_rate)

        print("\nfinal scores!")
        for player in self.players:
            print(player, player.fitness)
        # self.game_over_screen()

    # def game_over_screen(self):
    #     _font = pygame.font.SysFont('Purisa', 50)
    #     text_surface = _font.render('Game Over', False, (0, 0, 0))
    #     self.screen.blit(text_surface, (self.screen_w // 2 - text_surface.get_width() // 2,
    #                                     self.screen_h // 2 - text_surface.get_height() // 2))
    #     _font2 = pygame.font.SysFont('Purisa', 20)
    #     text_surface_2 = _font2.render('Press Enter to restart. ESC to quit', True, (0, 0, 0))
    #     self.screen.blit(text_surface_2, (self.screen_w // 2 - text_surface_2.get_width() // 2,
    #                                       self.screen_h // 2 + 30))

    def respawn_players(self):
        genes = [player.get_gene() for player in self.players]
        gene_pool = self.get_new_gene_pool(genes)

        for player, gene in zip(self.players, gene_pool):
            player.respawn(gene)

    def get_init_gene(self) -> np.ndarray:
        pass

    def get_new_gene_pool(self, genes: List[np.ndarray]) -> List[np.ndarray]:
        return [[]]*self.no_players
