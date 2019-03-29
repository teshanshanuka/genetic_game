from game_lib.evolution import createNewPopulation
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

        self.fitness_evol = []

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
                    # if player.score >= self.max_score:
                    #     print(player, "did it!!")
                    #     self.finalze()
                    #     return
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
        self.game_over_screen()

    def game_over_screen(self):
        """if anything is to display when game is over"""
        pass

    def respawn_players(self):
        genes = [player.get_gene() for player in self.players]
        fitnesses = [player.fitness for player in self.players]
        gene_pool = self.get_new_gene_pool(genes, fitnesses)

        for player, gene in zip(self.players, gene_pool):
            player.respawn(gene)


# TODO: From here onwards

    def get_init_gene(self) -> np.ndarray:
        return np.random.uniform(low=0.2, high=1.0, size=(210,))

    def get_new_gene_pool(self, genes: List[np.ndarray], fitnesses) -> List[np.ndarray]:
        """do stuff and create new gene pool using existing genes `genes`"""
        self.fitness_evol.append(fitnesses)
        return createNewPopulation(genes, fitnesses)

    def finalize(self):
        self.fitness_evol.append([player.fitness for player in self.players])
        # do something with fitnesses ???
