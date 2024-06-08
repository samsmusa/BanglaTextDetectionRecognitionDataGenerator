import os
from sklearn.model_selection import train_test_split
import shutil
import csv
import argparse


# Read file paths and labels from lable.txt

def main(base_dir_name, word_file, delimiter="\t", test_size=0.1):
    BASE_DIR_NAME = base_dir_name
    file_paths = []
    labels = []
    DELIMITER = delimiter
    with open(BASE_DIR_NAME + word_file, 'r') as file:
        reader = csv.reader(file, delimiter=DELIMITER, quoting=csv.QUOTE_NONE)
        for row in reader:
            path, label = row[0].strip(), " ".join(row[1:]).strip()
            file_paths.append(path)
            labels.append(label)

    # Split dataset into train and test sets
    train_paths, test_paths, train_labels, test_labels = train_test_split(file_paths, labels,
                                                                          test_size=test_size,
                                                                          random_state=42)

    # Create directories for train and test images
    os.makedirs(BASE_DIR_NAME + 'train/imgs/', exist_ok=True)
    os.makedirs(BASE_DIR_NAME + 'test/imgs/', exist_ok=True)

    # Move images to train and test directories
    with open(BASE_DIR_NAME + 'train/' + 'word.txt', 'w') as file:
        word_writer = csv.writer(file, delimiter=DELIMITER, quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL)
        for path, label in zip(train_paths, train_labels):
            shutil.copy2(path, BASE_DIR_NAME + 'train/imgs/')
            word_writer.writerow([path, label])

    with open(BASE_DIR_NAME + 'test/' + 'word.txt', 'w') as file:
        word_writer = csv.writer(file, delimiter=DELIMITER, quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL)
        for path, label in zip(test_paths, test_labels):
            shutil.copy2(path, BASE_DIR_NAME + 'test/imgs/')
            word_writer.writerow([path, label])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate train and test datasets for images")
    parser.add_argument("-b", "--base_dir", help="Path to the base directory")
    parser.add_argument("-w", "--word_file", help="Path to the word file")
    parser.add_argument("--delimiter", help="Delimiter for the word file (default: '\t')",
                        type=str, default="\t")
    parser.add_argument("--test_size",
                        help="Proportion of the dataset used for testing (default: 0.1)",
                        type=float, default=0.1)
    args = parser.parse_args()

    # Validate test_size argument
    if args.test_size <= 0 or args.test_size >= 1:
        raise ValueError("test_size must be within the range (0, 1).")

    main(args.base_dir, args.word_file, delimiter=args.delimiter, test_size=args.test_size)
