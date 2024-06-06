from btdr.tools import generate
import glob

import random

color = ["#403346", "#FF7E38", "#ae2121", "#2f261e", "#514058", "#470d7d", "#000", "#000", "#000",
         "#000", "#000"]
for index, font in enumerate(glob.glob("../fonts/*.ttf"), 42006):
    generate.generate_annotations(
        'text_data/test_top.txt', "../out", font, random.choice(range(18, 50)),
        color[random.choice
        (range(len(color)))], index,
        background_type=6
    )
