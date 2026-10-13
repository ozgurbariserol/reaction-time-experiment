"""Rapid image-sequence experiment (pygame).

Run from the repository root:
    python -m src.experiment --group male
    python -m src.experiment --group female

See README.md for details.
"""
import argparse
import os
import random
import sys
import time

import pygame

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

FPS = 10                 # image sequence rate (frames per second)
WINDOW_WIDTH = 1366
WINDOW_HEIGHT = 768
IMAGE_SIZE = 225         # images are drawn unscaled, centred on this square
TRIALS = 100
ANSWER_TIMEOUT_MS = 2000
IMAGE_EXTS = (".jpg", ".jpeg", ".png")

# Trial types (shown as "Soru Tipi" in the results file):
# 0 = distractor (T1) first, target (T2) 3 frames later (300 ms at 10 fps)
# 1 = no target shown (the question is still asked)
# 2 = target (T2) first, distractor (T1) 2 frames later
# 3 = target only
# 4 = distractor (T1) first, target (T2) 5 frames later (500 ms at 10 fps)
# 101 entries in the original list (21 x type 1, 20 x each other type);
# 100 are used per run after shuffling, so one type-1 trial is dropped at random.
MODES = [0] * 20 + [1] * 21 + [2] * 20 + [3] * 20 + [4] * 20

# The only difference between the two original programs: upper bound of the
# random insertion index y used by trial types 2 and 3.
GROUPS = {"male": {"y_max": 10}, "female": {"y_max": 11}}


class Experiment:
    def __init__(self, group, stimuli_dir, results_path):
        self.y_max = GROUPS[group]["y_max"]
        self.results_path = results_path
        self.main_dir = os.path.join(stimuli_dir, group, "main")
        self.target_dir = os.path.join(stimuli_dir, group, "target")
        self.distractor_dir = os.path.join(stimuli_dir, group, "distractor")
        self.desc_dir = os.path.join(stimuli_dir, group, "desc")
        for d in (self.main_dir, self.target_dir, self.distractor_dir):
            if not self.list_images(d):
                sys.exit(f"No images found in {d}\n"
                         "Add your own images or run: python src/make_placeholder_stimuli.py")
        self.modes = list(MODES)

        pygame.init()
        pygame.display.set_caption("Fotoğraf Testi")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.desc_images = self.load_desc()

    # ---- helpers -------------------------------------------------------
    @staticmethod
    def list_images(folder):
        if not os.path.isdir(folder):
            return []
        return sorted(os.path.join(folder, f) for f in os.listdir(folder)
                      if f.lower().endswith(IMAGE_EXTS))

    @staticmethod
    def load(path):
        return pygame.image.load(path)

    def load_desc(self):
        """Instruction slides desc/1..3 (optional); otherwise one text screen."""
        slides = []
        for n in (1, 2, 3):
            for ext in IMAGE_EXTS:
                p = os.path.join(self.desc_dir, f"{n}{ext}")
                if os.path.isfile(p):
                    slides.append(self.load(p))
                    break
        if slides:
            return slides
        surf = pygame.Surface((921, 521))
        font = pygame.font.Font(None, 36)
        lines = ["Ekranda hızlı bir görüntü dizisi gösterilecek.",
                 "Dizi bittiğinde B (evet) veya M (hayır) tuşuna basarak yanıt verin.",
                 "Her denemeye SPACE tuşu ile başlanır.",
                 "",
                 "Başlamak için SPACE tuşuna basın."]
        for i, line in enumerate(lines):
            t = font.render(line, True, (255, 255, 255))
            surf.blit(t, (surf.get_width() // 2 - t.get_width() // 2, 150 + i * 45))
        return [surf]

    @staticmethod
    def quit_requested(event):
        return event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)

    def quit(self):
        pygame.quit()
        sys.exit()

    def center(self, surface, dy=0):
        return (WINDOW_WIDTH // 2 - surface.get_width() // 2,
                WINDOW_HEIGHT // 2 - surface.get_height() // 2 + dy)

    def draw_plus(self):
        cx, cy, size, thick = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 50, 5
        white = pygame.Color("white")
        pygame.draw.rect(self.screen, white, pygame.Rect(cx - size // 2, cy - thick // 2, size, thick))
        pygame.draw.rect(self.screen, white, pygame.Rect(cx - thick // 2, cy - size // 2, thick, size))

    # ---- screens -------------------------------------------------------
    def description(self):
        index = 0
        w, h = 921, 521
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.desc_images[index], (self.screen.get_width() / 2 - w / 2,
                                                   self.screen.get_height() / 2 - h / 2))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if self.quit_requested(event):
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    index += 1
                    if index >= len(self.desc_images):
                        return
                    self.screen.fill((0, 0, 0))
                    self.screen.blit(self.desc_images[index], (self.screen.get_width() / 2 - w / 2,
                                                               self.screen.get_height() / 2 - h / 2))
                    pygame.display.flip()

    def wait_for_space(self):
        while True:
            self.screen.fill(pygame.Color("black"))
            self.draw_plus()
            pygame.display.update()
            for event in pygame.event.get():
                if self.quit_requested(event):
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
            self.clock.tick(60)

    def round_end(self):
        """White frame drawn where the images were shown."""
        box = 200
        pygame.draw.rect(self.screen, (255, 255, 255),
                         ((WINDOW_WIDTH - box) // 2, (WINDOW_HEIGHT - box) // 2, box, box), 2)
        pygame.display.flip()

    # ---- one trial -----------------------------------------------------
    def build_sequence(self, mode):
        images = [self.load(p) for p in self.list_images(self.main_dir)]
        random.shuffle(images)
        x = random.randint(6, 11)
        y = random.randint(1, self.y_max)
        target = self.load(random.choice(self.list_images(self.target_dir)))

        def distractor():
            return self.load(random.choice(self.list_images(self.distractor_dir)))

        if mode == 0:
            images.insert(x, target)
            images.insert(x - 3, distractor())
        elif mode == 2:
            images.insert(y, target)
            images.insert(y + 2, distractor())
        elif mode == 3:
            images.insert(y, target)
        elif mode == 4:
            images.insert(x, target)
            images.insert(x - 5, distractor())
        return images

    def write_result(self, mode, answer, response_time):
        # Same text format as the original programs.
        if answer == "None":
            line = f"Soru Tipi: {mode} ==> YANLIS(BOS)\n"
        else:
            # B (yes) is the correct answer for every type except 1, M (no) only for type 1.
            correct = (answer == "B") != (mode == 1)
            verdict = "DOGRU" if correct else "YANLIS"
            line = f"Soru Tipi: {mode} ==> {verdict} ==> CEVAPLAMA SURESI (ms): {response_time}\n"
        os.makedirs(os.path.dirname(self.results_path) or ".", exist_ok=True)
        with open(self.results_path, "a", encoding="utf-8") as f:
            f.write(line)

    def shown(self, mode):
        images = self.build_sequence(mode)
        self.wait_for_space()

        for img in images:
            self.screen.blit(img, (WINDOW_WIDTH // 2 - IMAGE_SIZE // 2, WINDOW_HEIGHT // 2 - IMAGE_SIZE // 2))
            pygame.display.flip()
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))

        # Answer phase
        self.screen.fill((0, 0, 0))
        start_time = pygame.time.get_ticks()
        self.round_end()
        font = pygame.font.Font(None, 36)
        text = font.render("B/M", 1, (255, 255, 255))
        self.screen.blit(text, self.center(text))
        pygame.display.flip()

        answer, response_time = None, None
        while answer is None:
            now = pygame.time.get_ticks()
            if now - start_time > ANSWER_TIMEOUT_MS:
                text = font.render("DAHA HIZLI OLUN!", 1, (255, 255, 255))
                self.screen.blit(text, self.center(text, 50))
                pygame.display.flip()
                pygame.time.wait(1000)
                answer = "None"
                break
            for event in pygame.event.get():
                if self.quit_requested(event):
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_b, pygame.K_m):
                    answer = "B" if event.key == pygame.K_b else "M"
                    response_time = now - start_time
                    break
            self.clock.tick(1000)

        self.write_result(mode, answer, response_time)
        if answer != "None":
            pygame.time.wait(1000)
        self.screen.fill((0, 0, 0))

    def run(self):
        self.description()
        random.shuffle(self.modes)
        for i in range(TRIALS):
            self.shown(self.modes[i])
        self.quit()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m src.experiment", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--group", choices=sorted(GROUPS), required=True,
                        help="which stimulus set / program variant to use")
    parser.add_argument("--stimuli", default=os.path.join(ROOT, "stimuli"), help="stimuli folder")
    parser.add_argument("--results", default=None,
                        help="results file (default: data/results_<group>.txt)")
    args = parser.parse_args(argv)
    results = args.results or os.path.join(ROOT, "data", f"results_{args.group}.txt")
    Experiment(args.group, args.stimuli, results).run()


if __name__ == "__main__":
    main()
