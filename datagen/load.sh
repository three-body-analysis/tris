mkdir -p data/zipped
python datagen/download.py
mdkir data/unzipped
for f in data/zipped/*.tar; do tar zxvf "$f" -C data/unzipped; done
python datagen/combine.py