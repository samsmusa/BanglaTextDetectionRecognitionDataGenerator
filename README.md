This repos for generating bangla text image for recognition and detection
for recognition
```python
python btdr/tools/generate.py --words_file ./text_data/n_2word.txt --output_folder ./annotations/ --font_dir ./fonts  
```
it will generate folder name `annotations` contains `annotations` folders and `annotations.
txt` file.
### Prepare dataset for training

after that we need to split dataset into `train` and `test` folder.
```python
python train_test_split.py base_dir "./" word_file "annotations.txt"
```