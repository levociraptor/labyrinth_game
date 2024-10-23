import os
from random import randint

from pygame import Surface
from pygame.image import load
from pygame.sprite import Sprite
from pygame.transform import scale


class GameObject(Sprite):
    sprite_filename: str | None = None
    sprite_extension: str = "png"
    width: int = 50
    height: int = 50
    color_key: tuple[int, int, int] = (245, 245, 245)

    def __init__(self, topleft_x: int, topleft_y: int):
        super().__init__()
        sprite_image_full_path = os.path.join("resources", f"{self.sprite_filename}.{self.sprite_extension}")
        self.image = scale(load(sprite_image_full_path), (self.width, self.height))
        self.image.set_colorkey(self.color_key)
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft_x, topleft_y

    def draw(self, surface: Surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_collided_with(self, another_object: "GameObject") -> bool:
        return self.rect.colliderect(another_object.rect)


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
