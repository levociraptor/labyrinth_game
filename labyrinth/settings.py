from dataclasses import dataclass

@dataclass
class SpeedSetings:
    player_speed: int
    slime_speed: int


def load_settings() -> SpeedSetings:
    return SpeedSetings(player_speed=6, slime_speed=6)
