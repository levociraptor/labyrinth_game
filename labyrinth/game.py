from random import randint

import pygame
from pygame.sprite import Group, spritecollide

from game_objects import GameObject, Player, Slime, Wall
from settings import load_settings
from wall_calculator import calculate_walls_coord





class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_speed = load_settings().player_speed
        self.slime_speed = load_settings().slime_speed
        self.context = self._compose_context()

    def _compose_context(self) -> dict[str, GameObject]:
        list_of_coords = calculate_walls_coord(
            self.screen.get_height(),
            self.screen.get_width(),
            Wall.width,
            Wall.height)

        walls = Group(*[Wall(x, y) for x, y in list_of_coords])

        context = {
            'player': Player((self.screen.get_width() // 2) - 30, self.screen.get_height() // 2),
            'walls': walls,
        }

        for i in range(1, 4):
            while True:
                slime_x = randint(61, 1219)
                slime_y = randint(61, 659)
                slime_rect = pygame.Rect(slime_x, slime_y, Slime.width, Slime.height)

                temp_sprite = pygame.sprite.Sprite()
                temp_sprite.rect = slime_rect

                if not pygame.sprite.spritecollideany(temp_sprite, walls):
                    context[f'slime_{i}'] = Slime(slime_x, slime_y)
                    break

        return context

    def init(self) -> None:
        pygame.init()

    def _draw_whole_screen(self) -> None:
        self.screen.fill("purple")
        self.context['player'].draw(self.screen)
        self.context['walls'].draw(self.screen)
        for i in range(3):
            self.context[f'slime_{i+1}'].draw(self.screen)

    def _check_slime_collision(self, direction_slimes: list[tuple[int, int]]) -> None:

        old_slimes_topleft = []

        for i in range(3):
            old_slimes_topleft.append(self.context[f'slime_{i+1}'].rect.topleft)

            self.context[f'slime_{i+1}'].rect = self.context[f'slime_{i+1}'].rect.move(direction_slimes[i])
            if spritecollide(self.context[f'slime_{i+1}'], self.context['walls'], dokill=False):
                direction_slimes[i] = self.context[f'slime_{i+1}'].direction_choicer(self.slime_speed)
                self.context[f'slime_{i+1}'].rect.topleft = old_slimes_topleft[i]

            if self.context['player'].is_collided_with(self.context[f'slime_{i+1}']):
                self.running = False

    def run(self) -> None:
        direction_slimes = []
        for i in range(3):
            direction = self.context[f'slime_{i+1}'].direction_choicer(self.slime_speed)
            direction_slimes.append(direction)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self._draw_whole_screen()
            pygame.display.flip()

            keys = pygame.key.get_pressed()

            old_player_topleft = self.context['player'].rect.topleft

            if keys[pygame.K_w]:
                self.context['player'].rect = self.context['player'].rect.move(0, -1 * self.player_speed)
            if keys[pygame.K_s]:
                self.context['player'].rect = self.context['player'].rect.move(0, 1 * self.player_speed)
            if keys[pygame.K_a]:
                self.context['player'].rect = self.context['player'].rect.move(-1 * self.player_speed, 0)
            if keys[pygame.K_d]:
                self.context['player'].rect = self.context['player'].rect.move(1 * self.player_speed, 0)

            if spritecollide(self.context['player'], self.context['walls'], dokill=False):
                self.context['player'].rect.topleft = old_player_topleft

            self._check_slime_collision(direction_slimes)

            self.clock.tick(60) / 1000

        pygame.quit()
