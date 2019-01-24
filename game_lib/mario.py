import threading
import pygame.time as ptime


class Mario(threading.Thread):
    def __init__(self, ID):
        super().__init__()
        self.ID = ID
        self.loc = [0, 0]
        self.jumping = False
        self.ducking = False
        self.done_running = False
        self.clock = ptime.Clock()
        self.score = 0
        self.jump_vel = None
        self.gravity = None
        self.wlim, self.hlim = None, None
        self.frame_rate = None
        self.events = []
        self.env_set = False

    def set_env(self, jump_vel, gravity, wlim, hlim, frame_rate):
        self.jump_vel = jump_vel
        self.gravity = gravity
        self.wlim, self.hlim = wlim, hlim
        self.frame_rate = frame_rate
        self.env_set = True

    def run(self):
        if not self.env_set:
            raise RuntimeError("Environment is not set before running")
        t = t_j = 0
        while not self.done_running:
            t += 1
            if self.jumping:
                if t_j == 0: # when jumping starts
                    self.events.append([t, "jump"])
                t_j += 1
                self.loc[1] = self.hlim - (self.jump_vel * t_j - 0.5 * self.gravity * t_j ** 2)
                if self.loc[1] > self.hlim:
                    self.jumping = False
                    t_j = 0
                    self.loc[1] = self.hlim

            self.clock.tick(self.frame_rate)

        self.score = t
        print("ID:", self.ID, "score:", self.score)
