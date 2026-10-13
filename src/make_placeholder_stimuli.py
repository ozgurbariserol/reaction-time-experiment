"""Generate neutral placeholder stimuli (coloured shapes, no people).

Usage:  python src/make_placeholder_stimuli.py [--out stimuli] [--groups male female]
"""
import argparse
import os
import random

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame  # noqa: E402

SIZE = 225
COLORS = [(220, 60, 60), (60, 160, 220), (80, 190, 100), (230, 180, 50),
          (160, 100, 200), (240, 130, 60), (60, 60, 60), (150, 150, 150)]


def draw_shape(index, color, bg):
    surf = pygame.Surface((SIZE, SIZE))
    surf.fill(bg)
    kind = index % 3
    if kind == 0:
        pygame.draw.circle(surf, color, (SIZE // 2, SIZE // 2), 80)
    elif kind == 1:
        pygame.draw.rect(surf, color, (45, 45, SIZE - 90, SIZE - 90))
    else:
        pygame.draw.polygon(surf, color, [(SIZE // 2, 30), (SIZE - 30, SIZE - 30), (30, SIZE - 30)])
    return surf


def make_set(folder, prefix, count, rng, bg):
    os.makedirs(folder, exist_ok=True)
    for i in range(count):
        color = rng.choice(COLORS)
        pygame.image.save(draw_shape(i, color, bg), os.path.join(folder, f"{prefix}{i + 1}.png"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="stimuli", help="output stimuli folder")
    parser.add_argument("--groups", nargs="+", default=["male", "female"])
    args = parser.parse_args()
    pygame.init()
    rng = random.Random(0)
    for group in args.groups:
        base = os.path.join(args.out, group)
        make_set(os.path.join(base, "main"), "main", 11, rng, (235, 235, 235))
        make_set(os.path.join(base, "target"), "target", 3, rng, (255, 250, 200))
        make_set(os.path.join(base, "distractor"), "distractor", 3, rng, (200, 235, 255))
    print(f"Placeholders written under {args.out}/")


if __name__ == "__main__":
    main()
