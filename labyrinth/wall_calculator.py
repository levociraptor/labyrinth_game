from random import randint


def calculate_walls_coord(
            screen_height: int,
            screen_width: int,
            wall_width: int,
            wall_height: int
        ) -> list[tuple[int, int]]:

    amount_of_horizontal_walls = screen_width // wall_width
    amount_of_vertical_walls = screen_height // wall_height - 2
    list_of_coords = []

    for wall_num in range(amount_of_horizontal_walls + 1):
        list_of_coords.extend([
            (wall_num * wall_width, 0),
            (wall_num * wall_width, screen_height - wall_height)
        ])

    for wall_num in range(1, amount_of_vertical_walls + 1):
        list_of_coords.extend([
            (0, wall_num * wall_height),
            (screen_width - wall_width, wall_num * wall_height)
        ])

    x_coord = (wall_width * 2) + 2
    while x_coord < screen_width:
        if x_coord == 610:
            x_coord += (wall_width * 2) + 2
            continue
        vertical_walls = [(x_coord, wall_width * i) for i in range(amount_of_vertical_walls + 1)]
        for _ in range(3):
            passage = randint(0, len(vertical_walls) - 1)
            vertical_walls.pop(passage)
        list_of_coords.extend(vertical_walls)

        x_coord += (wall_width * 2) + 2

    return list_of_coords
