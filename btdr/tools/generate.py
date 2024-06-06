import argparse
import csv
import pathlib
import random
import os

from typing import List, Tuple

from btdr import data_generator, utils


def generate_annotations(word_file="words.txt", output_folder='./output',
                         font_dir="./btdr/fonts/", font_sizes=None,
                         text_color=None, index_start=1, background_type=3):
    if font_sizes is None:
        font_sizes = range(15, 30)
    else:
        font_sizes = range(*font_sizes)
    if text_color is None:
        text_color = ["#403346", "#FF7E38", "#ae2121", "#2f261e", "#514058", "#470d7d"]
    DELIMITER = "\t"
    annotation_file = os.path.join(output_folder, "annotations.txt")

    utils.create_folder_not_exist(output_folder)
    utils.create_file_not_exist(annotation_file)
    font_files = [os.path.join(font_dir, f) for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f))]
    out_dir = os.path.join(output_folder, 'annotations')
    utils.create_folder_not_exist(out_dir)
    with open(annotation_file, "a") as file:
        word_writer = csv.writer(file, delimiter=DELIMITER, quoting=csv.QUOTE_NONE,
                                 escapechar='\\')
        with open(word_file, "r") as file:
            for i, word in enumerate(file.readlines(), index_start):
                print(repr(word))
                if i == 10:
                    break
                img, file_name = data_generator.FakeTextDataGenerator.generate(
                    index=i,
                    text=word.strip(),
                    font=random.choice(font_files),
                    out_dir=out_dir,
                    size=random.choice(font_sizes),
                    extension='png',
                    skewing_angle=0,
                    random_skew=False,
                    blur=1,
                    random_blur=True,
                    background_type=background_type,
                    distorsion_type=0,
                    distorsion_orientation=0,
                    is_handwritten=False,
                    name_format=1,
                    width=20,
                    alignment=0,
                    text_color=random.choice(text_color),
                    orientation=0,
                    space_width=1,
                    character_spacing=1,
                    margins=[1, 1, 1, 1],
                    fit=True,
                    output_mask=False,
                    word_split=True,
                    image_dir="./background",
                    output_path=True
                    # stroke_width: int = 0,
                    # stroke_fill: str = "#282828",
                    # image_mode: str = "RGB",
                    # output_bboxes: int = 0,
                )
                output_path = os.path.join("annotations/", os.path.basename(file_name.strip()))
                word_writer.writerow([output_path.strip(), word.strip()])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate annotations for images")
    parser.add_argument("-w",  "--words_file",help="Path to the file containing words")
    parser.add_argument("-o", "--output_folder", help="Path to the output annotation file")
    parser.add_argument("-fd", "--font_dir", help="Path to the font file", nargs="?",
                        default="./btdr/fonts", type=pathlib.Path)
    parser.add_argument("-fs", "--font_size", help="font sizes", nargs="?", type=Tuple[int, int],
                        default=None)
    parser.add_argument("-tc", "--text_color", help="color of text", nargs="?", default=None,
                        type=List[str])
    parser.add_argument("-t", "--index_start", help="starting index of image", nargs="?", type=int,
                        default=1)
    parser.add_argument("-bg", "--bg_type", help="background type of image", nargs="?", type=int,
                        default=3)
    args = parser.parse_args()

    generate_annotations(args.words_file, args.output_folder, args.font_dir, args.font_size,
                         args.text_color, args.index_start, background_type=args.bg_type)
