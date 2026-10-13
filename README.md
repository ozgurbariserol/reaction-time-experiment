# reaction-time-experiment

[Türkçe](README.tr.md)

A small pygame program that shows a rapid, randomly ordered sequence of images in full-screen and records the participant's key response and reaction time in milliseconds.

Written by hand for a data-collection study in 2023.

## What it measures

Each run has 100 trials. In a trial a fixation cross is shown until the participant presses SPACE, then a fast sequence (10 images per second) is shown. Depending on the trial type, one "target" image (T2) and, in most types, one "distractor" image (T1) are inserted into the shuffled base sequence. At the end of the sequence the participant answers with `B` (yes) or `M` (no) within 2 seconds. The program records whether the answer matched the expected one and the reaction time in ms.

Trial types (the number written to the results file as `Soru Tipi`):

| Type | Content |
|------|---------|
| 0 | distractor, then target 3 frames (300 ms) later |
| 1 | no target shown, but the question is still asked |
| 2 | target, then distractor 2 frames later |
| 3 | target only |
| 4 | distractor, then target 5 frames (500 ms) later |

The order of trial types and the image order are random on every run. For every type except 1, `B` (yes) is scored as correct; for type 1, `M` (no) is scored as correct. (What exactly the participant is asked is not documented in the code.)

## Requirements and setup

- Python 3.8+ (tested with 3.11)
- `pip install -r requirements.txt` (pygame)
- The window is fixed at 1366x768 and full-screen.

## Stimuli

No images are distributed with this project. Put your own images in `stimuli/` (see [stimuli/README.md](stimuli/README.md)) or generate neutral coloured-shape placeholders:

```
python src/make_placeholder_stimuli.py
```

## Run

From the repository root:

```
python -m src.experiment --group male
python -m src.experiment --group female
```

Options: `--stimuli DIR` (default `stimuli/`), `--results FILE` (default `data/results_<group>.txt`).

`--group` selects the stimulus sub-folder `stimuli/<group>/`. The original work consisted of two almost identical programs (one per group); the only logic difference was the upper bound of a random insertion position (10 vs 11), which is kept as a per-group setting. Everything else was merged.

## Keys

| Key | Action |
|-----|--------|
| SPACE | advance instructions / start a trial |
| B (yes) or M (no) | answer at the end of a sequence |
| ESC | quit (added in this version; the full-screen window had no exit) |

## Results file

One line is appended per trial to `data/results_<group>.txt` (git-ignored):

```
Soru Tipi: <type> ==> DOGRU|YANLIS ==> CEVAPLAMA SURESI (ms): <ms>
Soru Tipi: <type> ==> YANLIS(BOS)
```

The second form is written when no answer is given within 2 seconds ("DAHA HIZLI OLUN!" is shown). Reaction time is measured from the moment the answer prompt appears. The file is appended to, never overwritten, and does not contain a participant or session identifier.

## Known limits

- Randomness is not seeded and not logged, so the actual image order of a trial is not recorded.
- Only trial type, correctness and time are stored; there is no timestamp, participant ID, or the key actually pressed.
- Exactly 100 trials are used from a list of 101 type entries, so the number of type-1 trials per run is 20 or 21.
- Images are not scaled; they are drawn at a fixed position assuming about 225x225 px. The resolution is hard-coded.
- Key presses made before the answer prompt are not checked, and timing uses a simple frame clock; it is not calibrated for millisecond-precise presentation timing.
- Instruction slides are optional images; if absent a plain Turkish text screen is shown. On-screen texts are in Turkish.
- Insertion positions assume a base sequence of about 11 images; fewer images may change the ranges.
- The other components of the original project are not included in this repository.

## License

MIT, see [LICENSE](LICENSE).
