import pygame
from pygame.sprite import Group, spritecollide

from random import randint

from game_object import GameObject
from settings import Speed_setings
from wall_calculator import calculate_walls_coord


class Player(GameObject):
    sprite_filename = 'player'


class Wall(GameObject):
    sprite_filename = 'wall'
    width = 60
    height = 60


class Slime(GameObject):
    sprite_filename = 'slime_1'

    def direction_choicer(self, slime_speed: int) -> tuple[int, int]:
        direction = randint(1, 4)
        if direction == 1:
            return 0, -1 * slime_speed
        elif direction == 2:
            return 0, 1 * slime_speed
        elif direction == 3:
            return -1 * slime_speed, 0
        else:
            return 1 * slime_speed, 0


def compose_context(screen) -> dict[str, GameObject]:
    list_of_coords = calculate_walls_coord(screen.get_height(),
                                           screen.get_width(),
                                           Wall.width,
                                           Wall.height)

    walls = Group(*[Wall(x, y) for x, y in list_of_coords])

    context = {
        'player': Player((screen.get_width() // 2) - 30, screen.get_height() // 2),
        'walls': walls,
    }

    for i in range(1, 4):
        while True:
            slime_x = randint(61,1219)
            slime_y = randint(61,659)
            slime_rect = pygame.Rect(slime_x, slime_y, Slime.width, Slime.height)

            temp_sprite = pygame.sprite.Sprite()
            temp_sprite.rect = slime_rect

            if not pygame.sprite.spritecollideany(temp_sprite, walls):
                context[f'slime_{i}'] = Slime(slime_x, slime_y)
                break

    return context


def draw_whole_screen(screen, context: dict[str, GameObject]) -> None:
    screen.fill("purple")
    context['player'].draw(screen)
    context['walls'].draw(screen)
    for i in range(3):
        context[f'slime_{i+1}'].draw(screen)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    player_speed = Speed_setings.player_speed.value
    slime_speed = Speed_setings.slime_speed.value

    context = compose_context(screen)

    direction_slimes = []
    for i in range(3):
        direction_slimes.append(context[f'slime_{i+1}'].direction_choicer(slime_speed))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_whole_screen(screen, context)
        pygame.display.flip()

        keys = pygame.key.get_pressed()

        old_player_topleft = context['player'].rect.topleft

        if keys[pygame.K_w]:
            context['player'].rect = context['player'].rect.move(0, -1 * player_speed)
        if keys[pygame.K_s]:
            context['player'].rect = context['player'].rect.move(0, 1 * player_speed)
        if keys[pygame.K_a]:
            context['player'].rect = context['player'].rect.move(-1 * player_speed, 0)
        if keys[pygame.K_d]:
            context['player'].rect = context['player'].rect.move(1 * player_speed, 0)

        if spritecollide(context['player'], context['walls'], dokill=False):
            context['player'].rect.topleft = old_player_topleft

        old_slimes_topleft = []
        for i in range(3):
            old_slimes_topleft.append(context[f'slime_{i+1}'].rect.topleft)

            context[f'slime_{i+1}'].rect = context[f'slime_{i+1}'].rect.move(direction_slimes[i])
            if spritecollide(context[f'slime_{i+1}'], context['walls'], dokill=False):
                direction_slimes[i] = context[f'slime_{i+1}'].direction_choicer(slime_speed)
                context[f'slime_{i+1}'].rect.topleft = old_slimes_topleft[i]

            if context['player'].is_collided_with(context[f'slime_{i+1}']):
                running = False

        clock.tick(60) / 1000

    pygame.quit()


if __name__ == '__main__':
    main()