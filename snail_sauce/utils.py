from pygame.image import load
from pathlib import Path


def load_sprite(name, with_alpha=True):
    filename = Path(__file__).parent.parent / Path('assets/sprites/'+name + ".png")
    sprite = load(filename.resolve())
    return sprite.convert_alpha() if with_alpha else sprite.convert()
