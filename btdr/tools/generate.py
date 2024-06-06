import argparse
import csv
import random
import os

from btdr import data_generator, utils


def generate_annotations(word_file="words.txt", output_folder='./output',
                         font="./btdr/fonts/kalpurush.ttf", font_size=30,
                         text_color="#000", index_start=1, background_type=3):
    DELIMITER = "\t"
    annotation_file = os.path.join(output_folder, "annotations.txt")

    utils.create_folder_not_exist(output_folder)
    utils.create_file_not_exist(annotation_file)

    font_file = os.path.join(font)
    out_dir = os.path.join(output_folder, 'annotations')
    utils.create_folder_not_exist(out_dir)
    with open(annotation_file, "w") as file:
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
                    font=font_file,
                    out_dir=out_dir,
                    size=font_size,
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
                    text_color=text_color,
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
                output_path = os.path.join("./annotations/", os.path.basename(file_name.strip()))
                word_writer.writerow([output_path.strip(), word.strip()])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate annotations for images")
    parser.add_argument("words_file", help="Path to the file containing words")
    parser.add_argument("output_folder", help="Path to the output annotation file")
    parser.add_argument("font", help="Path to the font file", type=str)
    parser.add_argument("font_size", help="font size", type=int, default=30)
    parser.add_argument("text_color", help="color of text", default="#000", type=str)
    parser.add_argument("start_idx", help="starting index of image", type=int, default=1)
    args = parser.parse_args()

    generate_annotations(args.words_file, args.output_folder, args.font, args.font_size,
                         args.text_color, args.index_start)
