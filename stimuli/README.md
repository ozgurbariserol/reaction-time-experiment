# Stimuli / Uyaranlar

Put your own images here. This folder is intentionally empty in the repository
(image files are git-ignored). / Kendi görsellerinizi buraya koyun; depoda bu klasör bilerek boştur.

Layout (one sub-folder set per group, `male` and `female`) / Düzen:

```
stimuli/<group>/main/      base sequence images (about 225x225 px; jpg, jpeg, png)
stimuli/<group>/target/    target images ("T2"), one is picked at random per trial
stimuli/<group>/distractor/  distractor images ("T1"), one is picked at random per trial
stimuli/<group>/desc/      optional instruction slides 1.jpg, 2.jpg, 3.jpg
                           (if missing, a plain text instruction screen is shown)
```

Images are drawn unscaled, centred on a 225x225 area, so use roughly that size.
Görseller ölçeklenmez; yaklaşık 225x225 piksel kullanın.

No stimuli are distributed with this project. To try the program without real
images, generate neutral coloured-shape placeholders:

```
python src/make_placeholder_stimuli.py
```
